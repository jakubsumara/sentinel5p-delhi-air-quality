"""
Setup verification script for Sentinel-5P project.
Run this to check if all required packages are installed correctly.
"""

import sys

# Fix Windows encoding issues
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass  # If already wrapped, ignore

def check_package(package_name, import_name=None):
    """Check if a package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"[OK] {package_name} is installed")
        return True
    except ImportError:
        print(f"[MISSING] {package_name} is NOT installed")
        return False

def main():
    """Check all required packages."""
    print("=" * 60)
    print("Sentinel-5P Project - Environment Check")
    print("=" * 60)
    print()
    
    required_packages = [
        ("xarray", "xarray"),
        ("rioxarray", "rioxarray"),
        ("geopandas", "geopandas"),
        ("cartopy", "cartopy"),
        ("matplotlib", "matplotlib"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("earthengine-api", "ee"),
        ("cdsapi", "cdsapi"),
        ("rasterio", "rasterio"),
        ("netcdf4", "netCDF4"),  # Package name is netcdf4, but import is netCDF4
        ("jupyter", "jupyter"),
        ("tqdm", "tqdm"),
        ("scikit-learn", "sklearn"),
    ]
    
    print("Checking required packages...")
    print("-" * 60)
    
    results = []
    for package_name, import_name in required_packages:
        results.append(check_package(package_name, import_name))
    
    print()
    print("=" * 60)
    
    if all(results):
        print("[OK] All required packages are installed!")
        print()
        print("Next steps:")
        print("1. Set up Google Earth Engine: python -c 'import ee; ee.Authenticate()'")
        print("2. Or set up Copernicus Data Space credentials")
        print("3. Start with notebooks/01_data_download.ipynb")
    else:
        print("[WARNING] Some packages are missing!")
        print()
        print("Install missing packages with:")
        print("  pip install -r requirements.txt")
        print("  Or run: install.bat (Windows) or install.sh (Linux/Mac)")
        print("  Or use the notebook: notebooks/00_setup_verification.ipynb")
    
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Try to import and show versions
    print("\nPackage versions:")
    print("-" * 60)
    try:
        import xarray as xr
        print(f"xarray: {xr.__version__}")
    except:
        pass
    
    try:
        import pandas as pd
        print(f"pandas: {pd.__version__}")
    except:
        pass
    
    try:
        import numpy as np
        print(f"numpy: {np.__version__}")
    except:
        pass
    
    try:
        import ee
        print(f"earthengine-api: {ee.__version__}")
    except:
        pass

if __name__ == "__main__":
    main()
