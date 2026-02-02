"""
Google Earth Engine Data Download Script
Downloads Sentinel-5P data for Delhi NCR region using Google Earth Engine.
"""

import ee
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

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

def download_pollutant_data(pollutant_code, start_date, end_date, output_dir='data/processed'):
    """
    Download Sentinel-5P data for a specific pollutant.
    
    Parameters:
    -----------
    pollutant_code : str
        One of: 'NO2', 'SO2', 'CO', 'HCHO'
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
    output_dir : str
        Directory to save output files
    """
    if pollutant_code not in config.POLLUTANTS:
        print(f"[ERROR] Unknown pollutant: {pollutant_code}")
        return None
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    collection_id = pollutant_info['gee_collection']
    band_name = pollutant_info['gee_band']
    
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
            
            # Export to Google Drive (we'll download from there)
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

def get_time_series_data(pollutant_code, start_date, end_date):
    """
    Get time series of area-averaged concentrations.
    Returns a pandas DataFrame with daily values.
    """
    if pollutant_code not in config.POLLUTANTS:
        print(f"[ERROR] Unknown pollutant: {pollutant_code}")
        return None
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    collection_id = pollutant_info['gee_collection']
    band_name = pollutant_info['gee_band']
    
    print(f"\nGetting time series for {pollutant_info['name']}...")
    
    roi = get_delhi_roi()
    collection = ee.ImageCollection(collection_id)
    
    filtered = collection.filterDate(start_date, end_date).filterBounds(roi)
    
    # Get list of images with dates
    def get_image_info(image):
        date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')
        mean = image.select(band_name).reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=roi,
            scale=1000,
            maxPixels=1e9
        ).get(band_name)
        return ee.Feature(None, {'date': date, 'mean': mean})
    
    features = filtered.map(get_image_info)
    info_list = features.getInfo()['features']
    
    # Convert to DataFrame
    data = []
    for feature in info_list:
        props = feature['properties']
        if props['mean'] is not None:
            data.append({
                'date': props['date'],
                'value': props['mean']
            })
    
    df = pd.DataFrame(data)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df = df.set_index('date')
    
    return df

def main():
    """Main function."""
    print("="*60)
    print("Google Earth Engine - Sentinel-5P Data Download")
    print("="*60)
    
    # Initialize GEE
    if not initialize_gee():
        return
    
    # Get date range from config
    start_date = config.START_DATE
    end_date = config.END_DATE
    
    print(f"\nDate range: {start_date} to {end_date}")
    print(f"Region: Delhi NCR ({config.DELHI_ROI})")
    
    # Ask which pollutant to download
    print("\nAvailable pollutants:")
    for code, info in config.POLLUTANTS.items():
        print(f"  {code}: {info['name']} - {info['description']}")
    
    print("\nOptions:")
    print("  1. Download all pollutants (monthly composites)")
    print("  2. Download specific pollutant")
    print("  3. Get time series data only")
    print("  4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        # Download all pollutants
        for code in config.POLLUTANTS.keys():
            download_pollutant_data(code, start_date, end_date)
            print(f"\nWaiting 5 seconds before next pollutant...")
            import time
            time.sleep(5)
    
    elif choice == '2':
        # Download specific pollutant
        code = input("Enter pollutant code (NO2, SO2, CO, HCHO): ").strip().upper()
        if code in config.POLLUTANTS:
            download_pollutant_data(code, start_date, end_date)
        else:
            print("[ERROR] Invalid pollutant code")
    
    elif choice == '3':
        # Get time series
        code = input("Enter pollutant code (NO2, SO2, CO, HCHO): ").strip().upper()
        if code in config.POLLUTANTS:
            df = get_time_series_data(code, start_date, end_date)
            if df is not None and not df.empty:
                output_file = f"data/processed/{code}_timeseries.csv"
                os.makedirs('data/processed', exist_ok=True)
                df.to_csv(output_file)
                print(f"\n[OK] Time series saved to: {output_file}")
                print(f"Records: {len(df)}")
                print(f"\nFirst few values:")
                print(df.head())
    
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
