"""
Download HCHO Data from Google Earth Engine
Downloads only HCHO (Formaldehyde) data that may have been missed.
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
    """Get Delhi region of interest as Earth Engine geometry."""
    roi = ee.Geometry.Rectangle([
        config.DELHI_ROI['lon_min'],
        config.DELHI_ROI['lat_min'],
        config.DELHI_ROI['lon_max'],
        config.DELHI_ROI['lat_max']
    ])
    return roi

def download_hcho_data(start_date, end_date):
    """
    Download HCHO data for the date range.
    
    Parameters:
    -----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
    """
    pollutant_code = 'HCHO'
    pollutant_info = config.POLLUTANTS[pollutant_code]
    collection_id = pollutant_info['gee_collection']
    band_name = pollutant_info['gee_band']  # Should be 'tropospheric_HCHO_column_number_density'
    
    print(f"\n{'='*60}")
    print(f"Downloading {pollutant_info['name']} ({pollutant_code})")
    print(f"{'='*60}")
    print(f"Collection: {collection_id}")
    print(f"Date range: {start_date} to {end_date}")
    
    # Get collection
    collection = ee.ImageCollection(collection_id)
    
    # Filter by date and region
    roi = get_delhi_roi()
    filtered = collection.filterDate(start_date, end_date).filterBounds(roi)
    
    # Get collection size
    count = filtered.size().getInfo()
    print(f"Found {count} images")
    
    if count == 0:
        print("[WARNING] No images found for this date range")
        return None
    
    # Create monthly composites
    print("\nCreating monthly composites...")
    
    # Get list of months in date range
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    monthly_composites = []
    
    current = start
    while current < end:
        # Calculate month end
        if current.month == 12:
            month_end = current.replace(year=current.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = current.replace(month=current.month + 1, day=1) - timedelta(days=1)
        
        month_start_str = current.strftime('%Y-%m-%d')
        month_end_str = min(month_end, end).strftime('%Y-%m-%d')
        
        print(f"  Processing {current.strftime('%Y-%m')}...")
        
        # Filter for this month
        month_collection = filtered.filterDate(month_start_str, month_end_str)
        month_count = month_collection.size().getInfo()
        
        if month_count > 0:
            # Compute mean composite
            monthly_mean = month_collection.select(band_name).mean()
            
            # Export to Google Drive
            filename = f"Delhi_{pollutant_code}_{current.strftime('%Y%m')}"
            
            task = ee.batch.Export.image.toDrive(
                image=monthly_mean,
                description=filename,
                folder='Sentinel5P_Delhi',
                fileNamePrefix=filename,
                scale=1000,  # 1km resolution
                region=roi,
                fileFormat='GeoTIFF',
                crs='EPSG:4326'
            )
            
            task.start()
            monthly_composites.append({
                'month': current.strftime('%Y-%m'),
                'task_id': task.id,
                'filename': filename,
                'status': 'RUNNING'
            })
            
            print(f"    Started export task: {task.id}")
        else:
            print(f"    No images for this month")
        
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1, day=1)
        else:
            current = current.replace(month=current.month + 1, day=1)
    
    print(f"\n[OK] Started {len(monthly_composites)} export tasks")
    print("\nNote: Files will be exported to your Google Drive.")
    print("Check task status in: https://code.earthengine.google.com/tasks")
    print("Or wait for tasks to complete and download from Google Drive.")
    
    return monthly_composites

def main():
    """Main function."""
    print("="*60)
    print("Download HCHO (Formaldehyde) Data")
    print("="*60)
    
    # Initialize GEE
    if not initialize_gee():
        return
    
    # Get date range from config
    start_date = config.START_DATE
    end_date = config.END_DATE
    
    print(f"\nDate range: {start_date} to {end_date}")
    print(f"Region: Delhi NCR ({config.DELHI_ROI})")
    
    # Download HCHO data
    download_hcho_data(start_date, end_date)
    
    print("\n" + "="*60)
    print("Download started!")
    print("="*60)
    print("\nNext steps:")
    print("1. Wait for export tasks to complete (check: https://code.earthengine.google.com/tasks)")
    print("2. Download HCHO files from Google Drive folder 'Sentinel5P_Delhi'")
    print("3. Save them to: data/processed/")
    print("4. Run: python scripts/process_sentinel5p.py")

if __name__ == "__main__":
    main()
