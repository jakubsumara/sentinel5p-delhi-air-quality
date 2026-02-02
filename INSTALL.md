# Installation Guide

## Quick Installation

### Option 1: Using the Batch Script (Windows - Easiest)

Simply double-click `install.bat` or run in command prompt:
```bash
install.bat
```

### Option 2: Using Python Script

```bash
python scripts/install_packages.py
```

### Option 3: Using Jupyter Notebook

1. Open `notebooks/00_setup_verification.ipynb`
2. Run the first cell (uncomment the `install_packages()` line)
3. Wait for installation to complete
4. Restart the kernel

### Option 4: Manual Installation

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all packages
python -m pip install -r requirements.txt
```

## What Gets Installed

The installation includes:

### Core Data Processing
- `xarray` - For NetCDF/HDF5 data handling
- `rioxarray` - Geospatial extensions for xarray
- `geopandas` - Geospatial data operations
- `pandas`, `numpy` - Data manipulation

### Visualization
- `matplotlib` - Plotting
- `cartopy` - Map projections
- `seaborn` - Statistical plots
- `plotly` - Interactive plots

### Satellite Data Access
- `earthengine-api` - Google Earth Engine (recommended)
- `cdsapi` - Copernicus Data Space API

### Other Tools
- `jupyter` - Notebook environment
- `scikit-learn` - Machine learning (for clustering)
- `tqdm` - Progress bars

## Installation Time

- **Fast connection**: 5-10 minutes
- **Slow connection**: 15-30 minutes
- **Total size**: ~500 MB - 1 GB of packages

## Troubleshooting

### Cartopy Installation Fails

**Windows:**
```bash
# Try using conda instead
conda install -c conda-forge cartopy
```

**Linux:**
```bash
sudo apt-get install libproj-dev proj-data proj-bin libgeos-dev
pip install cartopy
```

**Mac:**
```bash
brew install proj geos
pip install cartopy
```

### Visual C++ Build Tools Error (Windows)

Some packages require Visual C++ Build Tools:
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "C++ build tools" workload
3. Restart and try installation again

### Memory/Storage Issues

If you run out of space:
1. Use virtual environment to isolate packages
2. Install packages one by one to identify large ones
3. Consider using Google Colab (cloud-based)

### Network/Timeout Issues

If downloads timeout:
```bash
# Increase timeout
python -m pip install --default-timeout=100 -r requirements.txt
```

### Install Specific Package Only

```bash
# Example: Install only Earth Engine
python -m pip install earthengine-api
```

## Verify Installation

After installation, verify everything works:

```bash
python scripts/setup_check.py
```

Or open the verification notebook:
```bash
jupyter notebook notebooks/00_setup_verification.ipynb
```

## Next Steps

1. ✅ Install packages (you are here)
2. Set up Google Earth Engine: `python -c "import ee; ee.Authenticate()"`
3. Or set up Copernicus Data Space credentials
4. Start with `notebooks/01_data_download.ipynb`

## Need Help?

- Check `QUICK_START.md` for quick reference
- Review `README.md` for detailed documentation
- Run `python scripts/setup_check.py` to diagnose issues
