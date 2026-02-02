@echo off
REM Setup script for creating a conda environment for Sentinel-5P project

echo ============================================================
echo Sentinel-5P Project - Conda Environment Setup
echo ============================================================
echo.

REM Check if conda is available
conda --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Conda is not installed or not in PATH
    echo Please install Anaconda or Miniconda first
    pause
    exit /b 1
)

echo Step 1: Creating conda environment 'sentinel5p'...
echo This may take a few minutes...
conda create -n sentinel5p python=3.11 -y
if errorlevel 1 (
    echo ERROR: Failed to create conda environment
    pause
    exit /b 1
)

echo.
echo Step 2: Activating environment and installing packages...
echo.

REM Activate environment and install packages
call conda activate sentinel5p
if errorlevel 1 (
    echo ERROR: Failed to activate environment
    pause
    exit /b 1
)

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing packages from requirements.txt...
echo This may take 5-10 minutes...
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

echo Step 5: Verifying installation...
python scripts\setup_check.py

echo.
echo ============================================================
echo Setup complete!
echo ============================================================
echo.
echo IMPORTANT: To use this environment in the future:
echo   1. Activate it: conda activate sentinel5p
echo   2. Then work on your project normally
echo.
echo Next steps:
echo   1. Make sure environment is activated: conda activate sentinel5p
echo   2. Set up Google Earth Engine: python -c "import ee; ee.Authenticate()"
echo   3. Open notebooks/00_setup_verification.ipynb to verify setup
echo.
pause
