"""
ERA5 Wind Data Download via Google Earth Engine
Alternative method using Google Earth Engine (if available).
"""

import ee
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def initialize_gee():
    """Initialize Google Earth Engine."""
    try:
        ee.Initialize(project='ee-jsumara')
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize Google Earth Engine: {e}")
        print("Run: python scripts/setup_gee.py first")
        return False

def get_delhi_roi():
    """Get Delhi region of interest (expanded for wind analysis)."""
    # Expand region slightly for wind trajectory analysis
    roi = ee.Geometry.Rectangle([
        config.DELHI_ROI['lon_min'] - 2,
        config.DELHI_ROI['lat_min'] - 2,
        config.DELHI_ROI['lon_max'] + 2,
        config.DELHI_ROI['lat_max'] + 2
    ])
    return roi

def download_era5_wind_month(year, month):
    """
    Download ERA5 wind data for a month using Google Earth Engine.
    
    Parameters:
    -----------
    year : int
        Year
    month : int
        Month (1-12)
    """
    print(f"Processing {year}-{month:02d}...")
    
    # ERA5 collection in Google Earth Engine
    # Note: ERA5 may not be available in GEE, this is a placeholder
    # Check: https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5
    
    try:
        # Try to access ERA5 (if available)
        collection = ee.ImageCollection('ECMWF/ERA5/DAILY')
        
        # Filter by date
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        filtered = collection.filterDate(start_date, end_date)
        
        # Select wind components
        # Note: Variable names may differ, check GEE catalog
        wind_data = filtered.select(['u_component_of_wind_10m', 'v_component_of_wind_10m'])
        
        # Get mean for the month
        monthly_mean = wind_data.mean()
        
        roi = get_delhi_roi()
        
        # Export to Google Drive
        filename = f"ERA5_wind_{year}{month:02d}"
        
        task = ee.batch.Export.image.toDrive(
            image=monthly_mean,
            description=filename,
            folder='ERA5_Delhi',
            fileNamePrefix=filename,
            scale=25000,  # ERA5 native resolution ~25km
            region=roi,
            fileFormat='GeoTIFF',
            crs='EPSG:4326'
        )
        
        task.start()
        print(f"  [OK] Started export task: {task.id}")
        return task
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        print("  Note: ERA5 may not be available in Google Earth Engine.")
        print("  Use CDS API method instead: python scripts/download_era5.py")
        return None

def main():
    """Main function."""
    print("="*60)
    print("ERA5 Wind Data Download via Google Earth Engine")
    print("="*60)
    print()
    print("Note: ERA5 data may not be available in Google Earth Engine.")
    print("If this fails, use the CDS API method: python scripts/download_era5.py")
    print()
    
    if not initialize_gee():
        return
    
    # Get date range from config
    start_date = config.START_DATE
    end_date = config.END_DATE
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    tasks = []
    current = start
    
    while current < end:
        task = download_era5_wind_month(current.year, current.month)
        if task:
            tasks.append(task)
        
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1, day=1)
        else:
            current = current.replace(month=current.month + 1, day=1)
    
    if tasks:
        print(f"\n[OK] Started {len(tasks)} export tasks")
        print("Check status: https://code.earthengine.google.com/tasks")
    else:
        print("\n[ERROR] No tasks started. Use CDS API method instead.")

if __name__ == "__main__":
    main()
