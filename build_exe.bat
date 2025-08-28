@echo off
echo Building Eye Tracker Executable...
echo.

REM Check if PyInstaller is installed
pip show pyinstaller > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PyInstaller is not installed.
    echo Installing PyInstaller...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install PyInstaller. Please install it manually:
        echo pip install pyinstaller
        pause
        exit /b 1
    )
)

REM Check if icon exists
if not exist icon.ico (
    echo WARNING: icon.ico not found. Running create_icon.py...
    python create_icon.py
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create icon. Continuing without an icon...
    )
)

echo Building executable with PyInstaller...
pyinstaller --name="Eye Tracking Mouse Control" --windowed --icon=icon.ico --onefile eye_tracker.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo The executable can be found in the 'dist' folder.
pause
