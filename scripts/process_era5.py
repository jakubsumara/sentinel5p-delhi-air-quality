"""
Process ERA5 Wind Data
Converts hourly ERA5 data to daily averages and calculates wind speed/direction.
"""

import os
import sys
import xarray as xr
import numpy as np
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def process_era5_month(nc_file, output_dir=None):
    """
    Process a single ERA5 monthly file to daily averages.
    
    Parameters:
    -----------
    nc_file : str
        Path to NetCDF file
    output_dir : str, optional
        Output directory (defaults to same as input)
    
    Returns:
    --------
    str
        Path to output file
    """
    if output_dir is None:
        output_dir = os.path.dirname(nc_file)
    
    output_file = os.path.join(output_dir, os.path.basename(nc_file).replace('.nc', '_daily.nc'))
    
    # Check if already processed
    if os.path.exists(output_file):
        print(f"  Already processed: {os.path.basename(output_file)}")
        return output_file
    
    print(f"  Processing {os.path.basename(nc_file)}...")
    
    try:
        # Open NetCDF file
        ds = xr.open_dataset(nc_file)
        
        # ERA5 uses 'valid_time' as the time coordinate, not 'time'
        # Rename it to 'time' for easier processing
        if 'valid_time' in ds.dims or 'valid_time' in ds.coords:
            if 'time' not in ds.dims:
                ds = ds.rename({'valid_time': 'time'})
        
        # Calculate daily average
        ds_daily = ds.resample(time='1D').mean()
        
        # Calculate wind speed (m/s)
        u = ds_daily['u']
        v = ds_daily['v']
        wind_speed = np.sqrt(u**2 + v**2)
        ds_daily['wind_speed'] = wind_speed
        ds_daily['wind_speed'].attrs = {
            'long_name': 'Wind speed',
            'units': 'm/s',
            'standard_name': 'wind_speed'
        }
        
        # Calculate wind direction (degrees, 0-360, where 0 is North)
        # atan2(-u, -v) gives direction wind is coming FROM
        wind_direction = np.arctan2(-u, -v) * 180 / np.pi
        wind_direction = (wind_direction + 360) % 360  # Convert to 0-360
        ds_daily['wind_direction'] = wind_direction
        ds_daily['wind_direction'].attrs = {
            'long_name': 'Wind direction (from)',
            'units': 'degrees',
            'standard_name': 'wind_from_direction',
            'comment': 'Direction wind is coming from (0=North, 90=East, 180=South, 270=West)'
        }
        
        # Add metadata
        ds_daily.attrs['processing'] = 'Daily average from hourly ERA5 data'
        ds_daily.attrs['original_file'] = os.path.basename(nc_file)
        
        # Save
        ds_daily.to_netcdf(output_file)
        ds.close()
        ds_daily.close()
        
        print(f"    [OK] Saved: {os.path.basename(output_file)}")
        return output_file
        
    except Exception as e:
        print(f"    [ERROR] Failed: {e}")
        return None

def process_all_era5(input_dir='data/era5', output_dir=None):
    """
    Process all ERA5 files in a directory.
    
    Parameters:
    -----------
    input_dir : str
        Directory containing ERA5 NetCDF files
    output_dir : str, optional
        Output directory (defaults to input_dir)
    """
    if output_dir is None:
        output_dir = input_dir
    
    print("="*60)
    print("Processing ERA5 Wind Data")
    print("="*60)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Find all NetCDF files
    nc_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.nc') and 'daily' not in f])
    
    if not nc_files:
        print(f"[ERROR] No ERA5 NetCDF files found in {input_dir}")
        return []
    
    print(f"Found {len(nc_files)} files to process...")
    print()
    
    processed_files = []
    for nc_file in nc_files:
        file_path = os.path.join(input_dir, nc_file)
        output_file = process_era5_month(file_path, output_dir)
        if output_file:
            processed_files.append(output_file)
    
    print()
    print("="*60)
    print(f"[OK] Processed {len(processed_files)} files")
    print("="*60)
    
    return processed_files

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process ERA5 wind data to daily averages')
    parser.add_argument('--input', default='data/era5', help='Input directory')
    parser.add_argument('--output', default=None, help='Output directory (defaults to input)')
    
    args = parser.parse_args()
    
    process_all_era5(args.input, args.output)

if __name__ == "__main__":
    main()
