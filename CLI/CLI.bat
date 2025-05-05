
---

**CLI.bat**
```batch
@echo off
:menu
cls
echo ==============================
echo    CivitAI Toolkit Launcher
echo ==============================
echo 1. Download Models (CiviFetch)
echo 2. Download Images (ImgPull)
echo 3. Exit
echo.

set /p choice="Enter option (1-3): "

if "%choice%"=="1" (
    echo Launching model downloader...
    python CiviFetch.py
    pause
    exit
)

if "%choice%"=="2" (
    echo WARNING: This tool cannot download GIFs or videos.
    echo Press any key to continue...
    pause >nul
    python ImgPull.py
    pause
    exit
)

if "%choice%"=="3" (
    exit
)

echo Invalid option. Exiting.
timeout /t 3 >nul
exit