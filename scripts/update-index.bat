@echo off
REM WMexperts Index Updater - Windows Batch Script
REM Run this file to update the index page with the latest blog posts

echo Updating WMexperts index page...
echo.

python update-index.py

if errorlevel 1 (
    echo.
    echo Error occurred. Make sure you have Python installed.
    echo Download from: https://www.python.org/downloads/
    pause
) else (
    echo.
    echo Index page updated successfully!
    pause
)
