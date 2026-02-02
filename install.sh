#!/bin/bash
# Installation script for Linux/Mac
# Installs all required packages for Sentinel-5P project

echo "============================================================"
echo "Sentinel-5P Project - Package Installation"
echo "============================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Step 1: Upgrading pip..."
python3 -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to upgrade pip"
    exit 1
fi

echo ""
echo "Step 2: Installing packages from requirements.txt..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some packages may have failed to install"
    echo "This is normal for some packages that require system libraries"
    echo ""
else
    echo ""
    echo "SUCCESS: All packages installed successfully!"
    echo ""
fi

echo "Step 3: Verifying installation..."
python3 scripts/setup_check.py

echo ""
echo "============================================================"
echo "Installation complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Set up Google Earth Engine: python3 -c 'import ee; ee.Authenticate()'"
echo "2. Open notebooks/00_setup_verification.ipynb to verify setup"
echo ""
