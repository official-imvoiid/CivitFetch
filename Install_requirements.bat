@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo       Secure Media Downloader - Dependencies Installer
echo ========================================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or newer from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python %PYTHON_VERSION%

:: Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not available. Attempting to install pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo Failed to install pip. Please install pip manually.
        pause
        exit /b 1
    )
)

echo.
echo Installing/Updating pip...
python -m pip install --upgrade pip

echo.
echo Installing required packages...
echo This may take a few minutes depending on your internet connection.
echo.

:: Install requirements
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Error installing dependencies. Please check your internet connection
    echo and make sure you have the necessary permissions.
    pause
    exit /b 1
)

echo.
echo ======================================================
echo             Installation Complete!
echo ======================================================
echo.
echo You can now run the applications Now
echo.
pause
