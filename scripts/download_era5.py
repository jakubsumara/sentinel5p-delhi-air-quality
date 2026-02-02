"""
ERA5 Wind Data Download Script
Downloads ERA5 reanalysis wind data (u-wind, v-wind) for Delhi NCR region.
"""

import sys
import os
from datetime import datetime, timedelta
import cdsapi
import xarray as xr

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def check_cds_setup():
    """Check if CDS API is set up."""
    try:
        # Try to initialize client with updated API endpoint
        # New API format: url should be https://cds.climate.copernicus.eu/api (no /v2)
        # Key should NOT have UID prefix (just the API key)
        client = cdsapi.Client()
        return True, client
    except Exception as e:
        print(f"[ERROR] CDS API not set up: {e}")
        print("\nTo set up CDS API:")
        print("1. Register at https://cds.climate.copernicus.eu/")
        print("2. Go to: https://cds.climate.copernicus.eu/#!/home")
        print("3. Click 'Your profile' -> 'API key'")
        print("4. Create file ~/.cdsapirc (or C:\\Users\\YourName\\.cdsapirc on Windows) with:")
        print("   url: https://cds.climate.copernicus.eu/api")
        print("   key: YOUR_API_KEY")
        print("\nNote: The key should NOT include the UID prefix anymore!")
        print("Update your cdsapi: pip install --upgrade cdsapi")
        return False, None

def download_era5_wind_month(year, month, output_dir='data/era5'):
    """
    Download ERA5 wind data for a specific month.
    
    Parameters:
    -----------
    year : int
        Year (e.g., 2023)
    month : int
        Month (1-12)
    output_dir : str
        Directory to save files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Delhi region bounds (slightly larger for wind analysis)
    area = [
        config.DELHI_ROI['lat_max'] + 2,  # North
        config.DELHI_ROI['lon_min'] - 2,  # West
        config.DELHI_ROI['lat_min'] - 2,  # South
        config.DELHI_ROI['lon_max'] + 2,  # East
    ]
    
    # Format dates
    month_str = f"{month:02d}"
    date_str = f"{year}-{month_str}"
    
    output_file = os.path.join(output_dir, f"era5_wind_{year}{month_str}.nc")
    
    # Check if file already exists
    if os.path.exists(output_file):
        print(f"  File already exists: {output_file}")
        return output_file
    
    print(f"  Downloading {date_str}...")
    
    try:
        client = cdsapi.Client()
        
        client.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'variable': [
                    'u_component_of_wind',
                    'v_component_of_wind',
                ],
                'pressure_level': str(config.ERA5['pressure_level']),
                'year': str(year),
                'month': month_str,
                'day': [f"{d:02d}" for d in range(1, 32)],  # All days
                'time': [
                    '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
                ],
                'area': area,  # [North, West, South, East]
                'format': 'netcdf',
            },
            output_file
        )
        
        print(f"    [OK] Saved to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"    [ERROR] Failed to download: {e}")
        return None

def download_era5_wind_range(start_date, end_date, output_dir='data/era5'):
    """
    Download ERA5 wind data for a date range.
    
    Parameters:
    -----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
    output_dir : str
        Directory to save files
    """
    print("="*60)
    print("ERA5 Wind Data Download")
    print("="*60)
    print(f"Date range: {start_date} to {end_date}")
    print(f"Pressure level: {config.ERA5['pressure_level']} hPa")
    print(f"Variables: {config.ERA5['variables']}")
    print()
    
    # Check CDS setup
    is_setup, client = check_cds_setup()
    if not is_setup:
        return None
    
    # Parse dates
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    downloaded_files = []
    
    # Download month by month
    current = start
    while current <= end:
        year = current.year
        month = current.month
        
        print(f"Processing {current.strftime('%Y-%m')}...")
        
        file_path = download_era5_wind_month(year, month, output_dir)
        if file_path:
            downloaded_files.append(file_path)
        
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1, day=1)
        else:
            current = current.replace(month=current.month + 1, day=1)
    
    print(f"\n[OK] Downloaded {len(downloaded_files)} files")
    print(f"Files saved in: {output_dir}")
    
    return downloaded_files

def get_daily_wind_average(nc_file):
    """
    Calculate daily average wind from hourly ERA5 data.
    
    Parameters:
    -----------
    nc_file : str
        Path to NetCDF file
    
    Returns:
    --------
    xarray.Dataset
        Daily averaged wind data
    """
    print(f"  Processing {os.path.basename(nc_file)}...")
    
    try:
        # Open NetCDF file
        ds = xr.open_dataset(nc_file)
        
        # Calculate daily average
        ds_daily = ds.resample(time='1D').mean()
        
        # Calculate wind speed and direction
        ds_daily['wind_speed'] = (ds_daily['u']**2 + ds_daily['v']**2)**0.5
        ds_daily['wind_direction'] = xr.ufuncs.arctan2(-ds_daily['u'], -ds_daily['v']) * 180 / 3.14159
        
        return ds_daily
        
    except Exception as e:
        print(f"    [ERROR] Failed to process: {e}")
        return None

def main():
    """Main function."""
    print("="*60)
    print("ERA5 Wind Data Download for Delhi NCR")
    print("="*60)
    print()
    
    # Get date range from config
    start_date = config.START_DATE
    end_date = config.END_DATE
    
    print("Options:")
    print("  1. Download ERA5 wind data (monthly files)")
    print("  2. Process downloaded files (calculate daily averages)")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        # Download data
        files = download_era5_wind_range(start_date, end_date)
        if files:
            print(f"\n[OK] Download complete! {len(files)} files downloaded.")
            print("\nNote: Files are large (~50-100 MB per month).")
            print("Next step: Process files to calculate daily averages.")
    
    elif choice == '2':
        # Process files
        era5_dir = config.PATHS['data_era5']
        if not os.path.exists(era5_dir):
            print(f"[ERROR] Directory not found: {era5_dir}")
            return
        
        nc_files = [f for f in os.listdir(era5_dir) if f.endswith('.nc')]
        
        if not nc_files:
            print(f"[ERROR] No NetCDF files found in {era5_dir}")
            return
        
        print(f"\nFound {len(nc_files)} files to process...")
        
        processed_files = []
        for nc_file in sorted(nc_files):
            file_path = os.path.join(era5_dir, nc_file)
            daily_data = get_daily_wind_average(file_path)
            
            if daily_data is not None:
                # Save daily average
                output_file = file_path.replace('.nc', '_daily.nc')
                daily_data.to_netcdf(output_file)
                processed_files.append(output_file)
                print(f"    [OK] Saved daily average: {output_file}")
        
        print(f"\n[OK] Processed {len(processed_files)} files")
    
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
