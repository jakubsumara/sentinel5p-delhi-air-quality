"""
Trajectory and Advection Analysis
Classifies pollution episodes as local vs advected based on wind patterns.
"""

import os
import sys
import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def load_era5_daily(file_path):
    """Load daily averaged ERA5 wind data."""
    try:
        ds = xr.open_dataset(file_path)
        return ds
    except Exception as e:
        print(f"[ERROR] Failed to load {file_path}: {e}")
        return None

def load_all_era5_daily(data_dir='data/era5'):
    """Load all daily ERA5 files and combine."""
    print("Loading ERA5 wind data...")
    
    daily_files = sorted([f for f in os.listdir(data_dir) if f.endswith('_daily.nc')])
    
    if not daily_files:
        print(f"[ERROR] No daily ERA5 files found in {data_dir}")
        return None
    
    print(f"Found {len(daily_files)} daily files")
    
    datasets = []
    for file in daily_files:
        file_path = os.path.join(data_dir, file)
        ds = load_era5_daily(file_path)
        if ds is not None:
            datasets.append(ds)
    
    if not datasets:
        return None
    
    # Combine all datasets
    combined = xr.concat(datasets, dim='time')
    combined = combined.sortby('time')
    
    print(f"[OK] Loaded {len(combined.time)} days of wind data")
    return combined

def calculate_wind_regime(u_wind, v_wind, wind_speed_threshold=4.0):
    """
    Classify wind regime based on speed and direction.
    
    Parameters:
    -----------
    u_wind, v_wind : array-like
        Wind components (m/s)
    wind_speed_threshold : float
        Threshold for low wind (m/s). Below this = local, above = advected.
        Default 4.0 m/s is appropriate for Delhi region.
    
    Returns:
    --------
    str
        Regime: 'local', 'advected_north', 'advected_south', etc.
    """
    wind_speed = np.sqrt(u_wind**2 + v_wind**2)
    
    # Low wind = local pollution (wind speed below threshold)
    if wind_speed < wind_speed_threshold:
        return 'local'
    
    # Calculate wind direction (where wind is coming FROM)
    wind_dir = np.arctan2(-u_wind, -v_wind) * 180 / np.pi
    wind_dir = (wind_dir + 360) % 360
    
    # Classify by direction
    if 315 <= wind_dir or wind_dir < 45:  # North
        return 'advected_north'
    elif 45 <= wind_dir < 135:  # East
        return 'advected_east'
    elif 135 <= wind_dir < 225:  # South
        return 'advected_south'
    elif 225 <= wind_dir < 315:  # West
        return 'advected_west'
    else:
        return 'advected_other'

def classify_pollution_regime(pollutant_data, era5_data, delhi_center=None):
    """
    Classify each day's pollution as local vs advected.
    
    Parameters:
    -----------
    pollutant_data : pandas.DataFrame
        Time series of pollutant concentrations (indexed by date)
    era5_data : xarray.Dataset
        ERA5 wind data
    delhi_center : dict, optional
        Delhi center coordinates
    
    Returns:
    --------
    pandas.DataFrame
        Time series with regime classification
    """
    if delhi_center is None:
        delhi_center = config.DELHI_CENTER
    
    print("\nClassifying pollution regimes...")
    
    # Get wind data at Delhi center
    wind_at_delhi = era5_data.sel(
        latitude=delhi_center['lat'],
        longitude=delhi_center['lon'],
        method='nearest'
    )
    
    # Since pollutant data is monthly, calculate monthly average wind conditions
    # Resample wind data to monthly averages
    wind_monthly = wind_at_delhi.resample(time='1MS').mean()  # 1MS = start of month
    
    # Extract values and ensure they're 1D
    u_values = wind_monthly['u'].values
    v_values = wind_monthly['v'].values
    speed_values = wind_monthly['wind_speed'].values
    dir_values = wind_monthly['wind_direction'].values
    
    # Flatten if multi-dimensional
    if u_values.ndim > 1:
        u_values = u_values.flatten()
        v_values = v_values.flatten()
        speed_values = speed_values.flatten()
        dir_values = dir_values.flatten()
    
    # Handle time - use start of month for matching
    time_values = pd.to_datetime(wind_monthly['time'].values)
    if isinstance(time_values, pd.DatetimeIndex):
        time_values = time_values
    elif time_values.ndim > 1:
        time_values = time_values.flatten()
    
    # Create DataFrame with monthly wind data
    wind_df = pd.DataFrame({
        'date': time_values,
        'u_wind': u_values,
        'v_wind': v_values,
        'wind_speed': speed_values,
        'wind_direction': dir_values
    })
    wind_df = wind_df.set_index('date')
    
    # Merge with pollutant data
    # Match by month (pollutant data is on 15th of month, wind is start of month)
    result = pollutant_data.copy()
    result['month_key'] = result.index.to_period('M')
    
    # Create month_key for wind_df
    wind_df_reset = wind_df.reset_index()
    wind_df_reset['month_key'] = wind_df_reset['date'].dt.to_period('M')
    wind_df_reset = wind_df_reset.set_index('month_key')
    
    # Merge on month_key
    result = result.merge(
        wind_df_reset[['u_wind', 'v_wind', 'wind_speed', 'wind_direction']], 
        left_on='month_key', right_index=True, how='left'
    )
    result = result.drop('month_key', axis=1)
    
    # Classify regime
    result['regime'] = result.apply(
        lambda row: calculate_wind_regime(row['u_wind'], row['v_wind']),
        axis=1
    )
    
    # Add binary classification
    result['is_local'] = result['regime'] == 'local'
    result['is_advected'] = result['regime'] != 'local'
    
    return result

def calculate_back_trajectory(era5_data, start_lon, start_lat, start_time, hours_back=72):
    """
    Calculate back-trajectory from a point.
    
    Parameters:
    -----------
    era5_data : xarray.Dataset
        ERA5 wind data
    start_lon, start_lat : float
        Starting coordinates
    start_time : datetime
        Starting time
    hours_back : int
        Number of hours to go back
    
    Returns:
    --------
    pandas.DataFrame
        Trajectory path with coordinates
    """
    trajectory = []
    
    current_lon = start_lon
    current_lat = start_lat
    current_time = start_time
    
    for hour in range(0, hours_back, 6):  # Every 6 hours
        time_step = start_time - timedelta(hours=hour)
        
        # Get wind at current location and time
        try:
            wind = era5_data.sel(
                time=time_step,
                latitude=current_lat,
                longitude=current_lon,
                method='nearest'
            )
            
            u = float(wind['u'].values)
            v = float(wind['v'].values)
            
            # Move backward (opposite direction of wind)
            # Wind direction is where wind comes FROM, so we move in that direction
            dt_hours = 6
            current_lon = current_lon - (u * dt_hours * 3600) / (111320 * np.cos(np.radians(current_lat)))
            current_lat = current_lat - (v * dt_hours * 3600) / 111320
            
            trajectory.append({
                'time': time_step,
                'lon': current_lon,
                'lat': current_lat,
                'u_wind': u,
                'v_wind': v
            })
        except:
            break
    
    return pd.DataFrame(trajectory)

def analyze_severe_episodes(pollutant_data, era5_data, threshold_percentile=90):
    """
    Identify severe pollution episodes and calculate their trajectories.
    
    Parameters:
    -----------
    pollutant_data : pandas.DataFrame
        Time series with regime classification
    era5_data : xarray.Dataset
        ERA5 wind data
    threshold_percentile : float
        Percentile threshold for severe episodes
    
    Returns:
    --------
    pandas.DataFrame
        Severe episodes with trajectory information
    """
    print(f"\nIdentifying severe episodes (>{threshold_percentile}th percentile)...")
    
    # Check if we have valid data
    if 'value' not in pollutant_data.columns:
        print("[WARNING] No 'value' column found")
        return pd.DataFrame()
    
    values = pollutant_data['value'].dropna()
    if len(values) == 0:
        print("[WARNING] No valid values found")
        return pd.DataFrame()
    
    threshold = np.percentile(values, threshold_percentile)
    severe_days = pollutant_data[pollutant_data['value'] >= threshold].copy()
    
    print(f"Found {len(severe_days)} severe episodes")
    
    # Calculate trajectories for severe episodes
    trajectories = []
    for date, row in severe_days.iterrows():
        traj = calculate_back_trajectory(
            era5_data,
            config.DELHI_CENTER['lon'],
            config.DELHI_CENTER['lat'],
            date,
            hours_back=72
        )
        
        if not traj.empty:
            # Get origin (furthest point back)
            origin = traj.iloc[-1]
            severe_days.loc[date, 'origin_lon'] = origin['lon']
            severe_days.loc[date, 'origin_lat'] = origin['lat']
            severe_days.loc[date, 'trajectory_distance'] = np.sqrt(
                (origin['lon'] - config.DELHI_CENTER['lon'])**2 +
                (origin['lat'] - config.DELHI_CENTER['lat'])**2
            ) * 111  # Convert to km
    
    return severe_days

def main():
    """Main function."""
    print("="*60)
    print("Trajectory and Advection Analysis")
    print("="*60)
    
    # Load ERA5 data
    era5_data = load_all_era5_daily()
    if era5_data is None:
        return
    
    # Load pollutant time series
    pollutants = ['NO2', 'SO2', 'CO', 'HCHO']
    results = {}
    
    for code in pollutants:
        ts_file = f"data/processed/{code}_timeseries.csv"
        if not os.path.exists(ts_file):
            print(f"[WARNING] Time series not found: {ts_file}")
            continue
        
        print(f"\n{'='*60}")
        print(f"Analyzing {code}")
        print(f"{'='*60}")
        
        # Load time series
        pollutant_ts = pd.read_csv(ts_file, index_col=0, parse_dates=True)
        
        # Check column name (might be 'value' or the pollutant name)
        if 'value' not in pollutant_ts.columns and len(pollutant_ts.columns) > 0:
            # Use first numeric column
            first_col = pollutant_ts.columns[0]
            pollutant_ts = pollutant_ts.rename(columns={first_col: 'value'})
        
        # Classify regimes
        classified = classify_pollution_regime(pollutant_ts, era5_data)
        
        # Analyze severe episodes (only if we have data)
        if not classified.empty and 'value' in classified.columns and classified['value'].notna().any():
            severe = analyze_severe_episodes(classified, era5_data)
        else:
            severe = pd.DataFrame()
        
        # Save results
        output_file = f"data/processed/{code}_classified.csv"
        classified.to_csv(output_file)
        print(f"[OK] Saved classified data to: {output_file}")
        
        if not severe.empty:
            severe_file = f"data/processed/{code}_severe_episodes.csv"
            severe.to_csv(severe_file)
            print(f"[OK] Saved severe episodes to: {severe_file}")
        
        # Print summary
        print(f"\nSummary for {code}:")
        print(f"  Total days: {len(classified)}")
        print(f"  Local days: {classified['is_local'].sum()} ({classified['is_local'].mean()*100:.1f}%)")
        print(f"  Advected days: {classified['is_advected'].sum()} ({classified['is_advected'].mean()*100:.1f}%)")
        print(f"  Severe episodes: {len(severe)}")
        
        results[code] = classified
    
    print("\n" + "="*60)
    print("[OK] Trajectory analysis complete!")
    print("="*60)

if __name__ == "__main__":
    main()
