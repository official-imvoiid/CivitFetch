@echo off
cls
echo Starting Secure Media Downloader...
echo.

:: Start the application
start /B python app.py

:: Wait for the server to start
echo Waiting for server to initialize...
:wait_loop
timeout /t 1 /nobreak >nul
curl -s http://127.0.0.1:7860/ >nul 2>&1
if %errorlevel% neq 0 (
    echo Server starting...
    goto wait_loop
)

:: Extra wait time to ensure UI is fully loaded
echo Server started! Allowing time for UI to initialize...
timeout /t 10 /nobreak >nul

:: Open in default browser
echo Opening in your default browser...
start http://127.0.0.1:7860/

echo.
echo If the browser doesn't open automatically, please navigate to:
echo http://127.0.0.1:7860/
echo.
echo Press Ctrl+C to stop the server when you're done.

:: Keep the window open
