"""
Create Map Visualizations
Generates 24-month maps, seasonal anomaly maps, and animations.
"""

import os
import sys
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def load_composite(pollutant_code, data_dir='data/processed'):
    """Load monthly composite for a pollutant."""
    file_path = os.path.join(data_dir, f"{pollutant_code}_monthly_composite.nc")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] Composite not found: {file_path}")
        return None
    
    try:
        ds = xr.open_dataset(file_path)
        # Get the data variable
        data_vars = [v for v in ds.data_vars if v not in ['spatial_ref']]
        if data_vars:
            da = ds[data_vars[0]]
        else:
            da = ds.to_array().squeeze()
        return da
    except Exception as e:
        print(f"[ERROR] Failed to load: {e}")
        return None

def create_monthly_map(pollutant_code, month_data, month_str, output_dir='outputs/maps'):
    """Create a map for a single month."""
    os.makedirs(output_dir, exist_ok=True)
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    
    fig = plt.figure(figsize=(12, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Set map extent
    extent = [
        config.DELHI_ROI['lon_min'] - 0.2,
        config.DELHI_ROI['lon_max'] + 0.2,
        config.DELHI_ROI['lat_min'] - 0.2,
        config.DELHI_ROI['lat_max'] + 0.2
    ]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    
    # Add map features
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, alpha=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.5)
    ax.add_feature(cfeature.RIVERS, linewidth=0.3, alpha=0.3)
    ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--')
    
    # Get coordinates
    if 'lon' in month_data.coords and 'lat' in month_data.coords:
        lon = month_data.lon.values
        lat = month_data.lat.values
    elif 'x' in month_data.coords and 'y' in month_data.coords:
        # GeoTIFF coordinates might be in different CRS
        # Try to get from bounds
        lon = month_data.x.values
        lat = month_data.y.values
    else:
        print(f"    [WARNING] Could not determine coordinates for {month_str}")
        return None
    
    # Get values
    values = month_data.values
    if values.ndim > 2:
        values = values.squeeze()
    
    # Create meshgrid if needed
    if len(lon.shape) == 1 and len(lat.shape) == 1:
        LON, LAT = np.meshgrid(lon, lat)
    else:
        LON, LAT = lon, lat
    
    # Plot data
    if np.any(~np.isnan(values)):
        im = ax.contourf(LON, LAT, values, 
                        transform=ccrs.PlateCarree(),
                        cmap='viridis', levels=20, alpha=0.8)
        plt.colorbar(im, ax=ax, label=f"{pollutant_info['name']} ({pollutant_info['unit']})",
                    shrink=0.8, pad=0.02)
    
    # Add Delhi center marker
    ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'], 
           'r*', markersize=20, transform=ccrs.PlateCarree(), 
           label='Delhi Center', zorder=10)
    
    # Add known sources
    for source_type, sources in config.KNOWN_SOURCES.items():
        for source in sources:
            ax.plot(source['lon'], source['lat'], 'ko', 
                   markersize=8, transform=ccrs.PlateCarree(), 
                   alpha=0.6, zorder=9)
    
    ax.set_title(f"{pollutant_info['name']} - {month_str}", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, f"{pollutant_code}_{month_str}_map.png")
    plt.savefig(output_file, dpi=config.VISUALIZATION['figure_dpi'],
                format=config.VISUALIZATION['figure_format'], bbox_inches='tight')
    plt.close()
    
    return output_file

def create_seasonal_anomaly_map(pollutant_code, output_dir='outputs/maps'):
    """Create seasonal anomaly maps."""
    os.makedirs(output_dir, exist_ok=True)
    
    composite = load_composite(pollutant_code)
    if composite is None:
        return
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    
    # Calculate annual mean
    if 'time' in composite.dims:
        annual_mean = composite.mean(dim='time')
    else:
        annual_mean = composite
    
    # Calculate seasonal means
    seasons_data = {}
    for season_name, months in config.SEASONS.items():
        # Filter by month
        if 'time' in composite.dims:
            season_mask = composite['time'].dt.month.isin([int(m) for m in months])
            season_composite = composite.where(season_mask, drop=True)
            if len(season_composite.time) > 0:
                season_mean = season_composite.mean(dim='time')
                # Calculate anomaly
                anomaly = season_mean - annual_mean
                seasons_data[season_name] = anomaly
    
    # Create subplot for each season
    n_seasons = len(seasons_data)
    if n_seasons == 0:
        print(f"[WARNING] No seasonal data for {pollutant_code}")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12),
                            subplot_kw={'projection': ccrs.PlateCarree()})
    axes = axes.flatten()
    
    extent = [
        config.DELHI_ROI['lon_min'] - 0.2,
        config.DELHI_ROI['lon_max'] + 0.2,
        config.DELHI_ROI['lat_min'] - 0.2,
        config.DELHI_ROI['lat_max'] + 0.2
    ]
    
    season_names = ['winter', 'summer', 'monsoon', 'post_monsoon']
    
    for idx, season_name in enumerate(season_names):
        ax = axes[idx]
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, alpha=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.5)
        ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--')
        
        if season_name in seasons_data:
            anomaly = seasons_data[season_name]
            
            # Get coordinates
            if 'lon' in anomaly.coords and 'lat' in anomaly.coords:
                lon = anomaly.lon.values
                lat = anomaly.lat.values
            else:
                continue
            
            values = anomaly.values
            if values.ndim > 2:
                values = values.squeeze()
            
            if len(lon.shape) == 1 and len(lat.shape) == 1:
                LON, LAT = np.meshgrid(lon, lat)
            else:
                LON, LAT = lon, lat
            
            if np.any(~np.isnan(values)):
                # Use diverging colormap for anomalies
                vmax = np.nanmax(np.abs(values))
                im = ax.contourf(LON, LAT, values,
                                transform=ccrs.PlateCarree(),
                                cmap='RdBu_r', levels=20, 
                                vmin=-vmax, vmax=vmax, alpha=0.8)
                plt.colorbar(im, ax=ax, label='Anomaly (mol/m²)',
                           shrink=0.6, pad=0.02)
            
            ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'],
                   'r*', markersize=15, transform=ccrs.PlateCarree(), zorder=10)
        
        ax.set_title(f"{season_name.capitalize()} Anomaly", fontsize=12, fontweight='bold')
    
    plt.suptitle(f"{pollutant_info['name']} - Seasonal Anomalies (vs Annual Mean)",
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, f"{pollutant_code}_seasonal_anomaly.png")
    plt.savefig(output_file, dpi=config.VISUALIZATION['figure_dpi'],
                format=config.VISUALIZATION['figure_format'], bbox_inches='tight')
    plt.close()
    
    print(f"[OK] Saved seasonal anomaly map: {output_file}")

def create_animation(pollutant_code, output_dir='outputs/animations'):
    """Create animation showing temporal evolution."""
    os.makedirs(output_dir, exist_ok=True)
    
    composite = load_composite(pollutant_code)
    if composite is None:
        return
    
    if 'time' not in composite.dims:
        print(f"[WARNING] No time dimension for {pollutant_code}")
        return
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    
    # Set up figure
    fig = plt.figure(figsize=(12, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    extent = [
        config.DELHI_ROI['lon_min'] - 0.2,
        config.DELHI_ROI['lon_max'] + 0.2,
        config.DELHI_ROI['lat_min'] - 0.2,
        config.DELHI_ROI['lat_max'] + 0.2
    ]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, alpha=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.5)
    ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--')
    
    # Get coordinates from first time step
    first_time = composite.isel(time=0)
    if 'lon' in first_time.coords and 'lat' in first_time.coords:
        lon = first_time.lon.values
        lat = first_time.lat.values
    else:
        print(f"[WARNING] Could not determine coordinates")
        return
    
    if len(lon.shape) == 1 and len(lat.shape) == 1:
        LON, LAT = np.meshgrid(lon, lat)
    else:
        LON, LAT = lon, lat
    
    # Get value range for consistent colormap
    all_values = composite.values
    vmin = np.nanmin(all_values)
    vmax = np.nanmax(all_values)
    
    # Initialize plot
    values = composite.isel(time=0).values
    if values.ndim > 2:
        values = values.squeeze()
    
    im = ax.contourf(LON, LAT, values,
                    transform=ccrs.PlateCarree(),
                    cmap='viridis', levels=20,
                    vmin=vmin, vmax=vmax, alpha=0.8)
    
    cbar = plt.colorbar(im, ax=ax, label=f"{pollutant_info['name']} ({pollutant_info['unit']})")
    
    ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'],
           'r*', markersize=20, transform=ccrs.PlateCarree(), zorder=10)
    
    title = ax.set_title(f"{pollutant_info['name']} - {composite.time.values[0]}",
                        fontsize=14, fontweight='bold')
    
    def animate(frame):
        ax.clear()
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, alpha=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.5)
        ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--')
        
        values = composite.isel(time=frame).values
        if values.ndim > 2:
            values = values.squeeze()
        
        im = ax.contourf(LON, LAT, values,
                        transform=ccrs.PlateCarree(),
                        cmap='viridis', levels=20,
                        vmin=vmin, vmax=vmax, alpha=0.8)
        
        ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'],
               'r*', markersize=20, transform=ccrs.PlateCarree(), zorder=10)
        
        time_str = str(composite.time.values[frame])[:7]  # YYYY-MM
        ax.set_title(f"{pollutant_info['name']} - {time_str}",
                    fontsize=14, fontweight='bold')
        
        return [im]
    
    anim = animation.FuncAnimation(fig, animate, frames=len(composite.time),
                                 interval=500, blit=False, repeat=True)
    
    output_file = os.path.join(output_dir, f"{pollutant_code}_animation.gif")
    anim.save(output_file, writer='pillow', fps=config.VISUALIZATION['animation_fps'])
    plt.close()
    
    print(f"[OK] Saved animation: {output_file}")

def main():
    """Main function."""
    print("="*60)
    print("Creating Map Visualizations")
    print("="*60)
    
    pollutants = ['NO2', 'SO2', 'CO', 'HCHO']
    
    for code in pollutants:
        print(f"\n{'='*60}")
        print(f"Creating maps for {code}")
        print(f"{'='*60}")
        
        # Load composite
        composite = load_composite(code)
        if composite is None:
            continue
        
        # Create seasonal anomaly map
        print("Creating seasonal anomaly map...")
        create_seasonal_anomaly_map(code)
        
        # Create animation
        print("Creating animation...")
        try:
            create_animation(code)
        except Exception as e:
            print(f"[WARNING] Animation failed: {e}")
            print("(This is okay - animations require additional dependencies)")
        
        # Create sample monthly maps (first, middle, last month)
        if 'time' in composite.dims:
            print("Creating sample monthly maps...")
            n_months = len(composite.time)
            sample_indices = [0, n_months//2, n_months-1]
            
            for idx in sample_indices:
                month_data = composite.isel(time=idx)
                time_str = str(composite.time.values[idx])[:7].replace('-', '')
                create_monthly_map(code, month_data, time_str)
    
    print("\n" + "="*60)
    print("[OK] Map visualizations complete!")
    print("="*60)
    print("\nOutputs saved in:")
    print("  - outputs/maps/ (static maps)")
    print("  - outputs/animations/ (animations)")

if __name__ == "__main__":
    main()
