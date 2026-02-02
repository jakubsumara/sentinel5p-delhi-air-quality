"""
Source Attribution Maps
Shows upwind origin zones and transport pathways during severe episodes.
"""

import os
import sys
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime, timedelta

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Import Delhi boundaries
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delhi_boundaries import get_delhi_boundary_polygon, get_delhi_center_contours

def add_delhi_roi_contour(ax):
    """Add Delhi administrative boundary."""
    try:
        # Get Delhi administrative boundary
        boundary = get_delhi_boundary_polygon()
        # Ensure coordinates are lists/arrays
        if isinstance(boundary['lon'], (list, tuple, np.ndarray)) and isinstance(boundary['lat'], (list, tuple, np.ndarray)):
            ax.plot(boundary['lon'], boundary['lat'], 'r-', linewidth=2.5, 
                    transform=ccrs.PlateCarree(), zorder=11, label='Delhi NCR Boundary', alpha=0.8)
    except Exception as e:
        print(f"    [WARNING] Could not plot Delhi boundary: {e}")
    
    return ax

def load_era5_daily(data_dir='data/era5'):
    """Load all daily ERA5 files."""
    import glob
    
    daily_files = sorted([f for f in os.listdir(data_dir) if f.endswith('_daily.nc')])
    
    if not daily_files:
        return None
    
    datasets = []
    for file in daily_files:
        file_path = os.path.join(data_dir, file)
        try:
            ds = xr.open_dataset(file_path)
            datasets.append(ds)
        except:
            continue
    
    if not datasets:
        return None
    
    combined = xr.concat(datasets, dim='time')
    combined = combined.sortby('time')
    return combined

def calculate_back_trajectory_simple(era5_data, start_lon, start_lat, start_date, hours_back=72):
    """
    Simple back-trajectory calculation.
    
    Parameters:
    -----------
    era5_data : xarray.Dataset
        ERA5 wind data
    start_lon, start_lat : float
        Starting coordinates
    start_date : datetime
        Starting date
    hours_back : int
        Hours to go back
    
    Returns:
    --------
    pandas.DataFrame
        Trajectory path
    """
    trajectory = []
    
    current_lon = start_lon
    current_lat = start_lat
    current_time = start_date
    
    # Step backward in 6-hour increments
    for hour in range(0, hours_back, 6):
        time_step = start_date - timedelta(hours=hour)
        
        try:
            # Get wind at current location and time
            wind = era5_data.sel(
                time=time_step,
                latitude=current_lat,
                longitude=current_lon,
                method='nearest'
            )
            
            u = float(wind['u'].values.flatten()[0] if wind['u'].values.ndim > 0 else wind['u'].values)
            v = float(wind['v'].values.flatten()[0] if wind['v'].values.ndim > 0 else wind['v'].values)
            
            # Move backward (opposite direction of wind)
            # Wind direction is where wind comes FROM
            dt_hours = 6
            # Convert m/s to degrees (approximate)
            # 1 m/s ≈ 0.000009 degrees/second at equator
            # At Delhi latitude (~28°), adjust for cos(lat)
            lat_factor = np.cos(np.radians(current_lat))
            lon_step = -(u * dt_hours * 3600) / (111320 * lat_factor)  # degrees
            lat_step = -(v * dt_hours * 3600) / 111320  # degrees
            
            current_lon = current_lon + lon_step
            current_lat = current_lat + lat_step
            
            trajectory.append({
                'time': time_step,
                'lon': current_lon,
                'lat': current_lat,
                'u_wind': u,
                'v_wind': v
            })
        except Exception as e:
            # If we can't get wind data, stop
            break
    
    return pd.DataFrame(trajectory)

def create_source_attribution_map(pollutant_code, output_dir='outputs/maps'):
    """Create source attribution map showing trajectories for severe episodes."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Load severe episodes
    severe_file = f"data/processed/{pollutant_code}_severe_episodes.csv"
    if not os.path.exists(severe_file):
        print(f"[WARNING] Severe episodes file not found: {severe_file}")
        return
    
    severe_df = pd.read_csv(severe_file, index_col=0, parse_dates=True)
    
    if severe_df.empty:
        print(f"[WARNING] No severe episodes for {pollutant_code}")
        return
    
    # Load ERA5 data
    print("Loading ERA5 wind data...")
    era5_data = load_era5_daily()
    if era5_data is None:
        print("[ERROR] Could not load ERA5 data")
        return
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    
    # Create map
    fig = plt.figure(figsize=(14, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Extended extent to show trajectories
    extent = [
        config.DELHI_ROI['lon_min'] - 5,  # Extended west
        config.DELHI_ROI['lon_max'] + 2,  # Extended east
        config.DELHI_ROI['lat_min'] - 2,  # Extended south
        config.DELHI_ROI['lat_max'] + 5   # Extended north (Punjab/Haryana)
    ]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    
    # Add map features
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.8)
    ax.add_feature(cfeature.RIVERS, linewidth=0.5, alpha=0.5)
    ax.add_feature(cfeature.LAND, alpha=0.3)
    # Configure gridlines to avoid overlap with legend
    gl = ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--', dms=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = True
    gl.bottom_labels = True
    
    # Calculate trajectories for severe episodes
    print(f"Calculating trajectories for {len(severe_df)} severe episodes...")
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(severe_df)))
    
    for idx, (date, row) in enumerate(severe_df.iterrows()):
        traj = calculate_back_trajectory_simple(
            era5_data,
            config.DELHI_CENTER['lon'],
            config.DELHI_CENTER['lat'],
            date,
            hours_back=72
        )
        
        if not traj.empty:
            # Plot trajectory
            ax.plot(traj['lon'], traj['lat'],
                   color=colors[idx], linewidth=2, alpha=0.6,
                   transform=ccrs.PlateCarree(),
                   label=f"{date.strftime('%Y-%m')}")
            
            # Mark origin (furthest point back)
            origin = traj.iloc[-1]
            ax.plot(origin['lon'], origin['lat'],
                   'o', color=colors[idx], markersize=10,
                   transform=ccrs.PlateCarree(), alpha=0.8)
    
    # Add Delhi ROI contour
    add_delhi_roi_contour(ax)
    
    # Mark Delhi center
    ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'],
           'r*', markersize=25, transform=ccrs.PlateCarree(),
           label='Delhi', zorder=10, markeredgecolor='black', markeredgewidth=1)
    
    # Mark known source regions
    for source_type, sources in config.KNOWN_SOURCES.items():
        for source in sources:
            marker = 's' if 'power' in source_type else '^' if 'industrial' in source_type else 'D'
            ax.plot(source['lon'], source['lat'], marker,
                   markersize=12, transform=ccrs.PlateCarree(),
                   color='darkred', alpha=0.7, zorder=9,
                   label=source['name'] if source == sources[0] else '')
    
    # Add regions labels
    ax.text(75.3, 30.1, 'Punjab\n(Crop Burning)', 
           transform=ccrs.PlateCarree(), fontsize=9,
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6, pad=0.5))
    ax.text(76.1, 29.1, 'Haryana\n(Crop Burning)', 
           transform=ccrs.PlateCarree(), fontsize=9,
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6, pad=0.5))
    
    ax.set_title(f"{pollutant_info['name']} - Source Attribution Map\n"
                f"Back-trajectories for Severe Episodes (72 hours)",
                fontsize=13, fontweight='bold', pad=20)
    
    # Improve legend placement to avoid overlap
    ax.legend(loc='upper left', fontsize=7, ncol=2, framealpha=0.9, 
              columnspacing=0.5, handlelength=1.5)
    
    plt.tight_layout(pad=2.5)
    
    output_file = os.path.join(output_dir, f"{pollutant_code}_source_attribution.png")
    plt.savefig(output_file, dpi=config.VISUALIZATION['figure_dpi'],
                format=config.VISUALIZATION['figure_format'], bbox_inches='tight')
    plt.close()
    
    print(f"[OK] Saved source attribution map: {output_file}")

def main():
    """Main function."""
    print("="*60)
    print("Creating Source Attribution Maps")
    print("="*60)
    
    pollutants = ['NO2', 'SO2', 'CO', 'HCHO']
    
    for code in pollutants:
        print(f"\n{'='*60}")
        print(f"Creating source attribution for {code}")
        print(f"{'='*60}")
        create_source_attribution_map(code)
    
    print("\n" + "="*60)
    print("[OK] Source attribution maps complete!")
    print("="*60)

if __name__ == "__main__":
    main()
