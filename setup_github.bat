@echo off
REM Setup script for GitHub repository (Windows)

echo ==========================================
echo GitHub Repository Setup
echo ==========================================

REM Initialize git if not already done
if not exist .git (
    echo Initializing git repository...
    git init
    echo [OK] Git repository initialized
) else (
    echo [OK] Git repository already initialized
)

REM Add all files
echo.
echo Adding files to git...
git add .

REM Show status
echo.
echo Current git status:
git status --short

echo.
echo ==========================================
echo Next Steps:
echo ==========================================
echo.
echo 1. Create a new repository on GitHub:
echo    - Go to: https://github.com/new
echo    - Repository name: sentinel5p-delhi-air-quality
echo    - Description: Sentinel-5P Air Pollution Dynamics over Delhi NCR
echo    - Choose Public or Private
echo    - DO NOT initialize with README, .gitignore, or license
echo.
echo 2. Connect local repository to GitHub:
echo    git remote add origin https://github.com/YOUR_USERNAME/sentinel5p-delhi-air-quality.git
echo.
echo 3. Commit and push:
echo    git commit -m "Initial commit: Complete Sentinel-5P analysis project"
echo    git branch -M main
echo    git push -u origin main
echo.
echo ==========================================
pause
