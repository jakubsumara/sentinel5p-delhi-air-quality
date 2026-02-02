"""
Process Sentinel-5P Data
Processes downloaded Sentinel-5P GeoTIFF files from Google Drive.
Applies quality checks, creates composites, and prepares data for analysis.
"""

import os
import sys
import glob
import xarray as xr
import rioxarray as rio
import numpy as np
import pandas as pd
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def load_sentinel5p_tiff(tiff_file):
    """
    Load Sentinel-5P GeoTIFF file.
    
    Parameters:
    -----------
    tiff_file : str
        Path to GeoTIFF file
    
    Returns:
    --------
    xarray.DataArray
        Loaded data with coordinates
    """
    try:
        # Load with rioxarray to preserve geospatial info
        da = rio.open_rasterio(tiff_file)
        
        # Remove band dimension if present
        if 'band' in da.dims:
            da = da.squeeze('band')
        
        # Rename to standard names
        if 'x' in da.dims:
            da = da.rename({'x': 'lon', 'y': 'lat'})
        
        return da
    except Exception as e:
        print(f"    [ERROR] Failed to load {tiff_file}: {e}")
        return None

def process_sentinel5p_files(input_dir='data/processed', pollutant_code=None):
    """
    Process all Sentinel-5P files for a pollutant.
    
    Parameters:
    -----------
    input_dir : str
        Directory containing GeoTIFF files
    pollutant_code : str, optional
        Pollutant code (NO2, SO2, CO, HCHO). If None, processes all.
    
    Returns:
    --------
    dict
        Dictionary with processed data arrays by month
    """
    print("="*60)
    print("Processing Sentinel-5P Data")
    print("="*60)
    print(f"Input directory: {input_dir}")
    print()
    
    # Find all GeoTIFF files
    if pollutant_code:
        pattern = os.path.join(input_dir, f"*{pollutant_code}*.tif*")
    else:
        pattern = os.path.join(input_dir, "*.tif*")
    
    tiff_files = glob.glob(pattern)
    
    if not tiff_files:
        print(f"[WARNING] No GeoTIFF files found matching pattern: {pattern}")
        print("\nNote: Files should be downloaded from Google Drive first.")
        print("They should be in the 'Sentinel5P_Delhi' folder.")
        return {}
    
    print(f"Found {len(tiff_files)} files to process...")
    print()
    
    # Group by pollutant and month
    processed_data = {}
    
    for tiff_file in sorted(tiff_files):
        filename = os.path.basename(tiff_file)
        print(f"  Processing {filename}...")
        
        # Parse filename: Delhi_POLLUTANT_YYYYMM
        parts = filename.replace('.tif', '').replace('.tiff', '').split('_')
        if len(parts) >= 3:
            code = parts[1]
            month_str = parts[2]
            
            da = load_sentinel5p_tiff(tiff_file)
            if da is not None:
                # Remove band dimension if present
                if 'band' in da.dims:
                    da = da.squeeze('band')
                
                # Clip to Delhi ROI (if coordinates exist)
                # Note: GeoTIFF from GEE uses x/y, not lon/lat directly
                # We'll use the full extent for now
                da_clipped = da
                
                # Store by pollutant and month
                if code not in processed_data:
                    processed_data[code] = {}
                processed_data[code][month_str] = da_clipped
                
                print(f"    [OK] Loaded {code} for {month_str}")
            else:
                print(f"    [ERROR] Failed to load")
        else:
            print(f"    [WARNING] Could not parse filename: {filename}")
    
    print()
    print("="*60)
    print(f"[OK] Processed data for {len(processed_data)} pollutants")
    print("="*60)
    
    return processed_data

def create_time_series(processed_data, pollutant_code, output_file=None):
    """
    Create time series of area-averaged concentrations.
    
    Parameters:
    -----------
    processed_data : dict
        Processed data from process_sentinel5p_files
    pollutant_code : str
        Pollutant code
    output_file : str, optional
        Output CSV file path
    
    Returns:
    --------
    pandas.DataFrame
        Time series data
    """
    if pollutant_code not in processed_data:
        print(f"[ERROR] No data found for {pollutant_code}")
        return None
    
    data_list = []
    
    for month_str, da in sorted(processed_data[pollutant_code].items()):
        # Calculate area average (handle NaN values)
        # Get values as numpy array
        values = np.array(da.values)
        
        # Flatten if multi-dimensional
        if values.ndim > 1:
            values = values.flatten()
        
        # Calculate mean excluding NaN
        valid_values = values[~np.isnan(values)]
        if len(valid_values) > 0:
            mean_value = float(np.nanmean(values))
        else:
            mean_value = np.nan
            print(f"    [WARNING] No valid data for {month_str}")
        
        # Create date from month string (YYYYMM)
        year = int(month_str[:4])
        month = int(month_str[4:6])
        date = pd.Timestamp(year=year, month=month, day=15)  # Mid-month
        
        data_list.append({
            'date': date,
            'value': mean_value,
            'month': month_str
        })
    
    df = pd.DataFrame(data_list)
    df = df.set_index('date').sort_index()
    
    if output_file:
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        df.to_csv(output_file)
        print(f"[OK] Saved time series to: {output_file}")
    
    return df

def save_processed_composite(processed_data, pollutant_code, output_dir='data/processed'):
    """
    Save processed monthly composites as NetCDF.
    
    Parameters:
    -----------
    processed_data : dict
        Processed data
    pollutant_code : str
        Pollutant code
    output_dir : str
        Output directory
    """
    if pollutant_code not in processed_data:
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine all months into one dataset
    data_arrays = []
    for month_str, da in sorted(processed_data[pollutant_code].items()):
        year = int(month_str[:4])
        month = int(month_str[4:6])
        date = pd.Timestamp(year=year, month=month, day=15)
        
        da = da.assign_coords(time=date)
        data_arrays.append(da)
    
    # Combine along time dimension
    combined = xr.concat(data_arrays, dim='time')
    combined = combined.sortby('time')
    
    # Add metadata
    pollutant_info = config.POLLUTANTS[pollutant_code]
    combined.attrs = {
        'pollutant': pollutant_code,
        'name': pollutant_info['name'],
        'unit': pollutant_info['unit'],
        'description': pollutant_info['description'],
        'region': 'Delhi NCR',
        'processing': 'Monthly composites from Google Earth Engine'
    }
    
    # Save
    output_file = os.path.join(output_dir, f"{pollutant_code}_monthly_composite.nc")
    combined.to_netcdf(output_file)
    print(f"[OK] Saved composite to: {output_file}")
    
    return output_file

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process Sentinel-5P data')
    parser.add_argument('--input', default='data/processed', help='Input directory with GeoTIFF files')
    parser.add_argument('--pollutant', default=None, help='Pollutant code (NO2, SO2, CO, HCHO)')
    parser.add_argument('--output', default='data/processed', help='Output directory')
    
    args = parser.parse_args()
    
    # Process files
    processed_data = process_sentinel5p_files(args.input, args.pollutant)
    
    if not processed_data:
        print("\n[INFO] No data to process.")
        print("Make sure you've downloaded files from Google Drive to:", args.input)
        return
    
    # Process each pollutant
    for code in processed_data.keys():
        print(f"\nProcessing {code}...")
        
        # Create time series
        ts_file = os.path.join(args.output, f"{code}_timeseries.csv")
        create_time_series(processed_data, code, ts_file)
        
        # Save composite
        save_processed_composite(processed_data, code, args.output)

if __name__ == "__main__":
    main()
