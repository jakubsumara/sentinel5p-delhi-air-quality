@echo off
REM Installation script for Windows
REM Installs all required packages for Sentinel-5P project

echo ============================================================
echo Sentinel-5P Project - Package Installation
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo.
echo Step 2: Installing packages from requirements.txt...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may have failed to install
    echo This is normal for some packages that require system libraries
    echo.
) else (
    echo.
    echo SUCCESS: All packages installed successfully!
    echo.
)

echo Step 3: Verifying installation...
python scripts\setup_check.py

echo.
echo ============================================================
echo Installation complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Set up Google Earth Engine: python -c "import ee; ee.Authenticate()"
echo 2. Open notebooks/00_setup_verification.ipynb to verify setup
echo.
pause
