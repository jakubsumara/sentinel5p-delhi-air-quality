#!/bin/bash
# Setup script for creating a conda environment for Sentinel-5P project (Linux/Mac)

echo "============================================================"
echo "Sentinel-5P Project - Conda Environment Setup"
echo "============================================================"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda is not installed or not in PATH"
    echo "Please install Anaconda or Miniconda first"
    exit 1
fi

echo "Step 1: Creating conda environment 'sentinel5p'..."
echo "This may take a few minutes..."
conda create -n sentinel5p python=3.11 -y
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create conda environment"
    exit 1
fi

echo ""
echo "Step 2: Activating environment and installing packages..."
echo ""

# Initialize conda for bash shell
eval "$(conda shell.bash hook)"
conda activate sentinel5p

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate environment"
    exit 1
fi

echo ""
echo "Step 3: Upgrading pip..."
python -m pip install --upgrade pip

echo ""
echo "Step 4: Installing packages from requirements.txt..."
echo "This may take 5-10 minutes..."
python -m pip install -r requirements.txt
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

echo "Step 5: Verifying installation..."
python scripts/setup_check.py

echo ""
echo "============================================================"
echo "Setup complete!"
echo "============================================================"
echo ""
echo "IMPORTANT: To use this environment in the future:"
echo "  1. Activate it: conda activate sentinel5p"
echo "  2. Then work on your project normally"
echo ""
echo "Next steps:"
echo "  1. Make sure environment is activated: conda activate sentinel5p"
echo "  2. Set up Google Earth Engine: python -c 'import ee; ee.Authenticate()'"
echo "  3. Open notebooks/00_setup_verification.ipynb to verify setup"
echo ""
