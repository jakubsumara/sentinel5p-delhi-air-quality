"""
Google Earth Engine Setup Script
This script helps you authenticate and set up Google Earth Engine.
"""

import os
import sys

def setup_gee():
    """Set up Google Earth Engine authentication."""
    print("="*60)
    print("Google Earth Engine Setup")
    print("="*60)
    print()
    
    try:
        import ee
        print("[OK] earthengine-api package is installed")
    except ImportError:
        print("[ERROR] earthengine-api is not installed!")
        print("Install it with: pip install earthengine-api")
        return False
    
    print()
    print("Step 1: Authenticating with Google Earth Engine...")
    print("This will open a browser window for authentication.")
    print()
    
    try:
        # Try to initialize (will prompt for auth if needed)
        ee.Initialize(project='ee-jsumara')
        print("[OK] Google Earth Engine is already authenticated!")
        print()
        print("Testing connection...")
        
        # Test with a simple operation
        test_collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
        count = test_collection.size().getInfo()
        print(f"[OK] Connection successful! Found {count} NO2 images in collection.")
        return True
        
    except Exception as e:
        if "Please authenticate" in str(e) or "credentials" in str(e).lower():
            print()
            print("Authentication required. Starting authentication process...")
            print()
            try:
                ee.Authenticate(project='ee-jsumara')
                print()
                print("[OK] Authentication successful!")
                print("Initializing Earth Engine...")
                ee.Initialize()
                print("[OK] Google Earth Engine initialized successfully!")
                return True
            except Exception as auth_error:
                print(f"[ERROR] Authentication failed: {auth_error}")
                print()
                print("Troubleshooting:")
                print("1. Make sure you have a Google account")
                print("2. Check your internet connection")
                print("3. Try running: python -c 'import ee; ee.Authenticate()'")
                return False
        else:
            print(f"[ERROR] Failed to initialize: {e}")
            return False

def check_gee_status():
    """Check if Google Earth Engine is set up correctly."""
    print("="*60)
    print("Google Earth Engine Status Check")
    print("="*60)
    print()
    
    try:
        import ee
        ee.Initialize()
        
        # Test access to Sentinel-5P collections
        collections = {
            'NO2': 'COPERNICUS/S5P/OFFL/L3_NO2',
            'SO2': 'COPERNICUS/S5P/OFFL/L3_SO2',
            'CO': 'COPERNICUS/S5P/OFFL/L3_CO',
            'HCHO': 'COPERNICUS/S5P/OFFL/L3_HCHO'
        }
        
        print("Testing access to Sentinel-5P collections...")
        print("-"*60)
        
        for name, collection_id in collections.items():
            try:
                collection = ee.ImageCollection(collection_id)
                count = collection.size().getInfo()
                print(f"[OK] {name}: {count} images available")
            except Exception as e:
                print(f"[ERROR] {name}: {str(e)[:50]}")
        
        print()
        print("[OK] Google Earth Engine is ready to use!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Google Earth Engine is not set up: {e}")
        print()
        print("Run this script to set up: python scripts/setup_gee.py")
        return False

def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check_gee_status()
    else:
        success = setup_gee()
        if success:
            print()
            print("="*60)
            print("Setup Complete!")
            print("="*60)
            print()
            print("You can now use Google Earth Engine in your scripts.")
            print("Example:")
            print("  import ee")
            print("  ee.Initialize()")
            print("  collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')")
            print()
            print("Next steps:")
            print("1. Check status: python scripts/setup_gee.py check")
            print("2. Start downloading data: python scripts/download_gee.py")
            print("3. Or use the notebook: notebooks/01_data_download.ipynb")

if __name__ == "__main__":
    main()
