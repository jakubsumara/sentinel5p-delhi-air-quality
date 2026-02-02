"""
Hotspot and Cluster Analysis
Identifies persistent source regions for pollution.
"""

import os
import sys
import xarray as xr
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import DBSCAN

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def load_pollutant_composite(pollutant_code, data_dir='data/processed'):
    """Load monthly composite for a pollutant."""
    file_path = os.path.join(data_dir, f"{pollutant_code}_monthly_composite.nc")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] Composite not found: {file_path}")
        return None
    
    try:
        ds = xr.open_dataset(file_path)
        return ds
    except Exception as e:
        print(f"[ERROR] Failed to load: {e}")
        return None

def calculate_persistent_hotspots(composite_data, percentile_threshold=90):
    """
    Identify persistent hotspots (areas consistently above threshold).
    
    Parameters:
    -----------
    composite_data : xarray.Dataset
        Monthly composite data
    percentile_threshold : float
        Percentile threshold for hotspots
    
    Returns:
    --------
    xarray.DataArray
        Hotspot mask (1 = hotspot, 0 = not)
    """
    # Get the data variable (handle different naming)
    data_vars = list(composite_data.data_vars)
    # Remove non-data variables
    data_vars = [v for v in data_vars if v not in ['spatial_ref']]
    
    if not data_vars:
        print("[ERROR] No data variables found")
        return None
    
    data_var = data_vars[0]
    data_array = composite_data[data_var]
    
    # Check if time dimension exists
    if 'time' in data_array.dims:
        mean_data = data_array.mean(dim='time')
    else:
        mean_data = data_array
    
    # Convert to numpy array and handle NaN
    values = np.array(mean_data.values).flatten()
    values = values[~np.isnan(values.astype(float))]
    
    if len(values) == 0:
        print("[WARNING] No valid data for hotspot calculation")
        return None
    
    # Calculate threshold
    threshold = np.percentile(values, percentile_threshold)
    
    # Create hotspot mask
    hotspots = (mean_data > threshold).astype(int)
    
    return hotspots

def identify_source_regions(hotspots, known_sources=None):
    """
    Map hotspots to known source regions.
    
    Parameters:
    -----------
    hotspots : xarray.DataArray
        Hotspot mask
    known_sources : dict, optional
        Dictionary of known sources from config
    
    Returns:
    --------
    pandas.DataFrame
        Source regions with coordinates
    """
    if known_sources is None:
        known_sources = config.KNOWN_SOURCES
    
    # Get hotspot coordinates
    hotspot_coords = np.where(hotspots.values == 1)
    lons = hotspots.lon.values[hotspot_coords[1]]
    lats = hotspots.lat.values[hotspot_coords[0]]
    
    # Create DataFrame
    source_df = pd.DataFrame({
        'lon': lons,
        'lat': lats
    })
    
    # Match to known sources
    source_df['source_type'] = 'unknown'
    source_df['distance_to_known'] = np.nan
    
    for source_type, sources in known_sources.items():
        for source in sources:
            distances = np.sqrt(
                (source_df['lon'] - source['lon'])**2 +
                (source_df['lat'] - source['lat'])**2
            ) * 111  # Convert to km
            
            # Mark if within 10 km of known source
            nearby = distances < 10
            source_df.loc[nearby, 'source_type'] = source_type
            source_df.loc[nearby, 'distance_to_known'] = distances[nearby]
            source_df.loc[nearby, 'known_source_name'] = source['name']
    
    return source_df

def cluster_hotspots(hotspot_coords, eps_km=5):
    """
    Cluster hotspots using DBSCAN.
    
    Parameters:
    -----------
    hotspot_coords : array-like
        Coordinates of hotspots (lon, lat)
    eps_km : float
        Maximum distance for clustering (km)
    
    Returns:
    --------
    numpy.ndarray
        Cluster labels
    """
    # Convert to radians for distance calculation
    coords_rad = np.radians(hotspot_coords)
    
    # Convert eps from km to approximate degrees
    eps_deg = eps_km / 111.0
    
    # Cluster
    clustering = DBSCAN(eps=eps_deg, min_samples=3, metric='haversine')
    labels = clustering.fit_predict(coords_rad)
    
    return labels

def analyze_seasonal_patterns(composite_data):
    """
    Analyze seasonal patterns in pollution.
    
    Parameters:
    -----------
    composite_data : xarray.Dataset
        Monthly composite data
    
    Returns:
    --------
    dict
        Seasonal statistics
    """
    # Add season to data
    seasons_map = {}
    for season, months in config.SEASONS.items():
        for month in months:
            seasons_map[int(month)] = season
    
    composite_data['season'] = ('time', [
        seasons_map[pd.Timestamp(t).month] for t in composite_data.time.values
    ])
    
    # Calculate seasonal means
    seasonal_means = composite_data.groupby('season').mean(dim='time')
    
    return seasonal_means

def main():
    """Main function."""
    print("="*60)
    print("Hotspot and Cluster Analysis")
    print("="*60)
    
    pollutants = ['NO2', 'SO2', 'CO', 'HCHO']
    
    for code in pollutants:
        print(f"\n{'='*60}")
        print(f"Analyzing {code}")
        print(f"{'='*60}")
        
        # Load composite
        composite = load_pollutant_composite(code)
        if composite is None:
            continue
        
        # Identify hotspots
        print("Identifying persistent hotspots...")
        hotspots = calculate_persistent_hotspots(composite)
        
        if hotspots is None:
            print("[WARNING] Could not calculate hotspots - skipping")
            continue
        
        # Map to known sources
        print("Mapping to known sources...")
        source_regions = identify_source_regions(hotspots)
        
        # Save results
        output_file = f"data/processed/{code}_hotspots.csv"
        source_regions.to_csv(output_file, index=False)
        print(f"[OK] Saved hotspots to: {output_file}")
        
        # Seasonal analysis
        print("Analyzing seasonal patterns...")
        seasonal = analyze_seasonal_patterns(composite)
        
        seasonal_file = f"data/processed/{code}_seasonal.nc"
        seasonal.to_netcdf(seasonal_file)
        print(f"[OK] Saved seasonal analysis to: {seasonal_file}")
        
        # Print summary
        print(f"\nSummary for {code}:")
        print(f"  Total hotspots: {len(source_regions)}")
        print(f"  Known sources matched: {(source_regions['source_type'] != 'unknown').sum()}")
        
        for source_type in source_regions['source_type'].unique():
            count = (source_regions['source_type'] == source_type).sum()
            print(f"    {source_type}: {count}")
    
    print("\n" + "="*60)
    print("[OK] Hotspot analysis complete!")
    print("="*60)

if __name__ == "__main__":
    main()
