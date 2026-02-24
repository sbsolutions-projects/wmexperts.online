# JSON-LD Structured Data Fix Script
param(
    [string]$BlogPostsPath = ".\blog-posts",
    [switch]$DryRun,
    [string[]]$TargetFiles = @()
)

$categoryMapping = @{
    'around' = 'Around SAP EWM'
    'enhance' = 'Enhance SAP EWM'
    'mfs' = 'SAP EWM MFS'
    'reveal' = 'Reveal SAP EWM'
    'understand' = 'Understand SAP EWM'
    'work' = 'Work in SAP EWM'
}

function Escape-JsonString {
    param([string]$text)
    if ([string]::IsNullOrEmpty($text)) { return "" }
    
    $text = $text -replace '\\', '\\'
    $text = $text -replace '"', '\"'
    $text = $text -replace [char]9, '\t'
    $text = $text -replace [char]10, '\n'
    $text = $text -replace [char]13, '\r'
    
    return $text
}

function Extract-MetaContent {
    param([string]$content, [string]$property)
    
    $pattern = 'property="' + $property + '"\s+content="([^"]*)"'
    if ($content -match $pattern) {
        return $matches[1]
    }
    return $null
}

function Extract-FirstImageUrl {
    param([string]$content)
    
    # Look for first img tag with src attribute
    if ($content -match '<img\s+[^>]*src="([^"]*)"') {
        $url = $matches[1]
        if ($url -and $url -ne "https://wmexperts.online/assets/images/placeholder.png") {
            return $url
        }
    }
    
    return "https://wmexperts.online/assets/images/placeholder.png"
}

function Get-FileCategory {
    param([string]$filePath)
    
    if ($filePath -match "\\blog-posts\\([^\\]+)\\") {
        return $matches[1]
    }
    return "other"
}

function Get-ArticleSlug {
    param([string]$fileName)
    
    return [System.IO.Path]::GetFileNameWithoutExtension($fileName)
}

if ($TargetFiles.Count -gt 0) {
    $htmlFiles = @()
    foreach ($file in $TargetFiles) {
        if (Test-Path $file) {
            $htmlFiles += Get-Item $file
        }
    }
} else {
    $htmlFiles = Get-ChildItem -Path $BlogPostsPath -Filter "*.html" -Recurse
}

$results = @()

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Match the entire script tag including newlines
    $scriptPattern = '(?s)<script type="application/ld\+json">.*?</script>'
    
    if ($content -match $scriptPattern) {
        $category = Get-FileCategory $file.FullName
        $slug = Get-ArticleSlug $file.Name
        
        $title = Extract-MetaContent $content "og:title"
        $description = Extract-MetaContent $content "og:description"
        $published = Extract-MetaContent $content "article:published_time"
        $modified = Extract-MetaContent $content "article:modified_time"
        $imageUrl = Extract-FirstImageUrl $content
        
        if ($title -match "^(.*?)\s*\|\s*WMexperts") {
            $title = $matches[1]
        }
        
        if ([string]::IsNullOrEmpty($published)) {
            $published = "2024-01-01"
        }
        if ([string]::IsNullOrEmpty($modified)) {
            $modified = $published
        }
        
        # Ensure ISO 8601 format
        if ($published -notmatch 'T') {
            $published = $published + "T00:00:00Z"
        }
        if ($modified -notmatch 'T') {
            $modified = $modified + "T00:00:00Z"
        }
        
        $categoryDisplay = $categoryMapping[$category]
        if ([string]::IsNullOrEmpty($categoryDisplay)) {
            $categoryDisplay = $category
        }
        
        $titleEscaped = Escape-JsonString $title
        $descriptionEscaped = Escape-JsonString $description
        
        $newJsonLd = @"
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "BlogPosting",
  "headline": "$titleEscaped",
  "description": "$descriptionEscaped",
  "image": "$imageUrl",
  "datePublished": "$published",
  "dateModified": "$modified",
  "author": {
    "@type": "Person",
    "name": "Hendrik"
  },
  "publisher": {
    "@type": "Organization",
    "name": "WMexperts",
    "logo": {
      "@type": "ImageObject",
      "url": "https://wmexperts.online/assets/favicon/favicon-32x32.png"
    }
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://wmexperts.online/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "$categoryDisplay",
      "item": "https://wmexperts.online/blog-posts/$category/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "$titleEscaped",
      "item": "https://wmexperts.online/blog-posts/$category/$slug.html"
    }
  ]
}
</script>
"@
        
        # Replace all ld+json scripts with new ones (in case there are multiple)
        $origPattern = '(?s)<!-- Structured Data -->.*?</script>'
        $newContent = $content -replace $origPattern, "<!-- Structured Data -->`r`n$newJsonLd"
        
        if ($newContent -ne $content) {
            if (!$DryRun) {
                Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
            }
            
            $results += [PSCustomObject]@{
                File = $file.Name
                Category = $category
                Title = $title
                Published = $published
                Modified = $modified
                Image = $imageUrl
                Status = if ($DryRun) { "Would be fixed" } else { "Fixed" }
            }
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JSON-LD Structured Data Fix Results" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($results.Count -eq 0) {
    Write-Host "No files needed fixing." -ForegroundColor Green
} else {
    $results | ForEach-Object {
        Write-Host "File: $($_.File)" -ForegroundColor Green
        Write-Host "  Category: $($_.Category)" -ForegroundColor Yellow
        Write-Host "  Title: $($_.Title)"
        Write-Host "  Published: $($_.Published)"
        Write-Host "  Image: $($_.Image)"
        Write-Host "  Status: $($_.Status)" -ForegroundColor Cyan
        Write-Host ""
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total processed: $($results.Count) files" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "DRY RUN MODE - No files were modified" -ForegroundColor Yellow
    Write-Host "Run with -DryRun:$false to apply changes" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
