"""
Google Earth Engine Helper Functions
Common functions for working with Sentinel-5P data in Google Earth Engine.
"""

import ee
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def initialize_gee():
    """Initialize Google Earth Engine. Returns True if successful."""
    try:
        ee.Initialize()
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

def get_sentinel5p_collection(pollutant_code, start_date=None, end_date=None):
    """
    Get filtered Sentinel-5P collection for a pollutant.
    
    Parameters:
    -----------
    pollutant_code : str
        One of: 'NO2', 'SO2', 'CO', 'HCHO'
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format
    end_date : str, optional
        End date in 'YYYY-MM-DD' format
    
    Returns:
    --------
    ee.ImageCollection
        Filtered image collection
    """
    if pollutant_code not in config.POLLUTANTS:
        raise ValueError(f"Unknown pollutant: {pollutant_code}")
    
    collection_id = config.POLLUTANTS[pollutant_code]['gee_collection']
    collection = ee.ImageCollection(collection_id)
    
    roi = get_delhi_roi()
    collection = collection.filterBounds(roi)
    
    if start_date and end_date:
        collection = collection.filterDate(start_date, end_date)
    
    return collection

def create_monthly_composite(collection, band_name, month_start, month_end):
    """
    Create monthly composite from image collection.
    
    Parameters:
    -----------
    collection : ee.ImageCollection
        Image collection to composite
    band_name : str
        Name of the band to composite
    month_start : str
        Start date in 'YYYY-MM-DD' format
    month_end : str
        End date in 'YYYY-MM-DD' format
    
    Returns:
    --------
    ee.Image
        Monthly mean composite
    """
    filtered = collection.filterDate(month_start, month_end)
    composite = filtered.select(band_name).mean()
    return composite

def calculate_area_average(image, band_name, geometry=None):
    """
    Calculate area-averaged value for an image.
    
    Parameters:
    -----------
    image : ee.Image
        Image to calculate average for
    band_name : str
        Name of the band
    geometry : ee.Geometry, optional
        Geometry to calculate over (defaults to Delhi ROI)
    
    Returns:
    --------
    float
        Area-averaged value
    """
    if geometry is None:
        geometry = get_delhi_roi()
    
    stats = image.select(band_name).reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000,  # 1km resolution
        maxPixels=1e9
    )
    
    return stats.getInfo()[band_name]

def export_image_to_drive(image, filename, folder='Sentinel5P_Delhi', scale=1000):
    """
    Export image to Google Drive.
    
    Parameters:
    -----------
    image : ee.Image
        Image to export
    filename : str
        Filename prefix
    folder : str
        Google Drive folder name
    scale : float
        Resolution in meters
    
    Returns:
    --------
    ee.batch.Task
        Export task
    """
    roi = get_delhi_roi()
    
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=filename,
        folder=folder,
        fileNamePrefix=filename,
        scale=scale,
        region=roi,
        fileFormat='GeoTIFF',
        crs='EPSG:4326'
    )
    
    task.start()
    return task

def get_task_status(task_id):
    """Get status of an Earth Engine task."""
    # Note: This requires the task object, not just the ID
    # For checking by ID, use the web interface or REST API
    pass

def create_seasonal_composite(collection, band_name, season_months):
    """
    Create seasonal composite from collection.
    
    Parameters:
    -----------
    collection : ee.ImageCollection
        Image collection
    band_name : str
        Band name
    season_months : list
        List of month numbers (1-12) for the season
    
    Returns:
    --------
    ee.Image
        Seasonal mean composite
    """
    # This is a simplified version - you'd need to filter by month
    # For full implementation, filter collection by month and then composite
    filtered = collection.select(band_name)
    composite = filtered.mean()
    return composite

def mask_clouds(image, max_cloud_fraction=0.3):
    """
    Mask clouds from Sentinel-5P image.
    Note: Sentinel-5P doesn't have cloud mask like optical sensors,
    but we can use quality flags.
    
    Parameters:
    -----------
    image : ee.Image
        Sentinel-5P image
    max_cloud_fraction : float
        Maximum cloud fraction (0-1)
    
    Returns:
    --------
    ee.Image
        Masked image
    """
    # Sentinel-5P uses quality flags instead of cloud mask
    # This is a placeholder - actual implementation depends on product
    return image

# Example usage functions
def example_get_no2_data():
    """Example: Get NO2 data for last month."""
    if not initialize_gee():
        return None
    
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    collection = get_sentinel5p_collection(
        'NO2',
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    count = collection.size().getInfo()
    print(f"Found {count} NO2 images")
    
    return collection

if __name__ == "__main__":
    # Test the helpers
    print("Testing Google Earth Engine helpers...")
    
    if initialize_gee():
        print("[OK] Google Earth Engine initialized")
        
        roi = get_delhi_roi()
        print(f"[OK] Delhi ROI created: {roi.getInfo()}")
        
        collection = get_sentinel5p_collection('NO2', '2024-01-01', '2024-01-31')
        count = collection.size().getInfo()
        print(f"[OK] Found {count} NO2 images for January 2024")
    else:
        print("[ERROR] Failed to initialize")
