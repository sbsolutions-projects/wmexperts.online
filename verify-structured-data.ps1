# Script to verify JSON-LD structured data in blog posts
param(
    [string]$BlogPostsPath = ".\blog-posts",
    [string]$OutputFile = ".\structured-data-report.txt"
)

$issues = @()
$processed = 0
$healthy = 0

$htmlFiles = Get-ChildItem -Path $BlogPostsPath -Filter "*.html" -Recurse
Write-Host "Scanning $($htmlFiles.Count) HTML files..." -ForegroundColor Cyan
Write-Host ""

foreach ($file in $htmlFiles) {
    $processed++
    $filePath = $file.FullName
    $fileName = $file.Name
    $relPath = $file.FullName -replace [regex]::Escape($BlogPostsPath), "blog-posts"
    
    $content = Get-Content -Path $filePath -Raw
    $fileIssues = @()
    
    # Extract meta tags
    $publishedDateMatch = $null
    if ($content -match 'property="article:published_time"\s+content="([^"]*)"') {
        $publishedDateMatch = $matches[1]
    }
    
    # Extract JSON-LD BlogPosting section
    $jsonStartIdx = $content.IndexOf('<script type="application/ld+json">')
    if ($jsonStartIdx -eq -1) {
        $issues += @{File = $relPath; Issue = "JSON-LD script tag not found"}
        continue
    }
    
    $jsonArrayStart = $content.IndexOf('[', $jsonStartIdx)
    $jsonArrayEnd = $content.IndexOf(']', $jsonArrayStart)
    
    if ($jsonArrayStart -eq -1 -or $jsonArrayEnd -eq -1) {
        $issues += @{File = $relPath; Issue = "JSON array structure not found"}
        continue
    }
    
    $jsonString = $content.Substring($jsonArrayStart, $jsonArrayEnd - $jsonArrayStart + 1)
    
    try {
        $jsonData = ConvertFrom-Json $jsonString -ErrorAction Stop
    } catch {
        $issues += @{File = $relPath; Issue = "JSON parsing failed: $($_.Exception.Message)"}
        continue
    }
    
    # Find BlogPosting
    $blogPosting = $jsonData | Where-Object { $_.'@type' -eq 'BlogPosting' }
    
    if (-not $blogPosting) {
        $fileIssues += "@type 'BlogPosting' not found"
    } else {
        # Verify required fields
        if ($blogPosting.'@type' -ne 'BlogPosting') {
            $fileIssues += "@type is '$($blogPosting.'@type')' instead of 'BlogPosting'"
        }
        
        if (-not $blogPosting.author) {
            $fileIssues += "author field missing"
        } elseif ($blogPosting.author.name -ne 'Hendrik') {
            $fileIssues += "author is '$($blogPosting.author.name)' instead of 'Hendrik'"
        }
        
        if (-not $blogPosting.datePublished) {
            $fileIssues += "datePublished field missing"
        } elseif ($publishedDateMatch -and $blogPosting.datePublished -ne $publishedDateMatch) {
            $fileIssues += "datePublished mismatch: JSON says '$($blogPosting.datePublished)' but meta tag says '$publishedDateMatch'"
        }
        
        if (-not $blogPosting.headline -or $blogPosting.headline -eq 'Article Title') {
            $fileIssues += "headline missing or placeholder"
        }
        
        if (-not $blogPosting.image) {
            $fileIssues += "image field missing"
        } elseif ($blogPosting.image -eq 'https://wmexperts.online/assets/images/placeholder.png') {
            $fileIssues += "image uses placeholder ("  + $blogPosting.image  + ")"
        } elseif (-not ($blogPosting.image -match '^https://wmexperts\.online/assets/images/')) {
            $fileIssues += "image URL has wrong path: '$($blogPosting.image)'"
        }
        
        if (-not $blogPosting.publisher) {
            $fileIssues += "publisher field missing"
        } elseif ($blogPosting.publisher.name -ne 'WMexperts') {
            $fileIssues += "publisher is '$($blogPosting.publisher.name)' instead of 'WMexperts'"
        }
    }
    
    if ($fileIssues.Count -gt 0) {
        $issues += @{File = $relPath; Issues = $fileIssues}
    } else {
        $healthy++
        Write-Host "OK $fileName" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "STRUCTURED DATA VERIFICATION REPORT" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files processed: $processed"
Write-Host "Healthy files: $healthy" -ForegroundColor Green
Write-Host "Files with issues: $($issues.Count)" -ForegroundColor $(if ($issues.Count -gt 0) { 'Red' } else { 'Green' })
Write-Host ""

if ($issues.Count -gt 0) {
    Write-Host "FILES REQUIRING FIXES:" -ForegroundColor Red
    Write-Host ""
    
    $reportLines = @()
    $reportLines += "STRUCTURED DATA VERIFICATION REPORT"
    $reportLines += "===================================="
    $reportLines += ""
    $reportLines += "Generated: $(Get-Date)"
    $reportLines += "Total files processed: $processed"
    $reportLines += "Healthy files: $healthy"
    $reportLines += "Files with issues: $($issues.Count)"
    $reportLines += ""
    $reportLines += "FILES REQUIRING FIXES:"
    $reportLines += "====================="
    
    foreach ($issue in $issues) {
        Write-Host $issue.File -ForegroundColor Yellow
        $reportLines += ""
        $reportLines += $issue.File
        
        if ($issue.Issues) {
            foreach ($detail in $issue.Issues) {
                Write-Host "  - $detail" -ForegroundColor Red
                $reportLines += "  - $detail"
            }
        } else {
            Write-Host "  - $($issue.Issue)" -ForegroundColor Red
            $reportLines += "  - $($issue.Issue)"
        }
    }
    
    $reportLines | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host ""
    Write-Host "Report saved to: $OutputFile" -ForegroundColor Cyan
} else {
    Write-Host "All files have valid structured data!" -ForegroundColor Green
}
