# Quick Start Guide

## Step 1: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

**Note:** Some packages may take a few minutes to install. If you encounter errors:
- On Windows, you may need Visual C++ Build Tools for some packages
- Cartopy may require additional system libraries (PROJ, GEOS)

## Step 2: Verify Installation

```bash
# Run the setup check script
python scripts/setup_check.py

# Or open the verification notebook
jupyter notebook notebooks/00_setup_verification.ipynb
```

## Step 3: Choose Your Data Access Method

### Option A: Google Earth Engine (Recommended - Minimal Storage)

1. **Authenticate:**
   ```python
   import ee
   ee.Authenticate()  # Opens browser for authentication
   ee.Initialize()
   ```

2. **Test access:**
   ```python
   import ee
   ee.Initialize()
   s5p = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
   print(f"Collection size: {s5p.size().getInfo()}")
   ```

### Option B: Copernicus Data Space (Alternative)

1. Register at https://dataspace.copernicus.eu/
2. Generate API token
3. Store credentials (we'll create a script for this)

## Step 4: Update Configuration

Edit `config.py` to set your desired time period:
```python
START_DATE = '2022-01-01'  # Adjust to 24 months ago
END_DATE = '2024-01-01'    # Adjust to current date
```

## Step 5: Start Analysis

Open the first analysis notebook:
```bash
jupyter notebook notebooks/01_data_download.ipynb
```

## Troubleshooting

### Package Installation Issues

**Cartopy installation fails:**
- Windows: May need to install via conda: `conda install -c conda-forge cartopy`
- Linux: `sudo apt-get install libproj-dev proj-data proj-bin libgeos-dev`

**Earth Engine authentication fails:**
- Make sure you have a Google account
- Try: `ee.Authenticate(auth_mode='notebook')`

**NetCDF/HDF5 issues:**
- Install h5py: `pip install h5py`
- Install netCDF4: `pip install netcdf4`

### Storage Issues

If you're running low on storage:
1. Use Google Earth Engine (processes in cloud)
2. Process data in batches and delete raw files
3. Use external storage for `data/raw/` directory

## Next Steps

1. ✅ Complete setup (you are here)
2. Download/access data (next step)
3. Process and analyze
4. Create visualizations
5. Write report

## Getting Help

- Check `README.md` for detailed documentation
- Review `PROJECT_PLAN.md` for project overview
- Run `python scripts/setup_check.py` to diagnose issues
