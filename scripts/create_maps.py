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
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Import Delhi boundaries
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

# Major power plants in Delhi NCR region (active 2022-2024) with types and colors
# Only plants within or near Delhi ROI (76.5-78.0°E, 28.0-29.0°N)
MAJOR_POWER_PLANTS = {
    'coal': [
        {'name': 'Dadri TPS', 'lon': 77.5500, 'lat': 28.5500, 'capacity': '1820 MW'},  # Greater Noida - active
        {'name': 'Indraprastha TPS', 'lon': 77.2500, 'lat': 28.6200, 'capacity': '270 MW'},  # Active
        {'name': 'Panipat TPS', 'lon': 76.9600, 'lat': 29.3900, 'capacity': '920 MW'},  # Haryana - near
        {'name': 'Rajghat TPS', 'lon': 77.2300, 'lat': 28.6400, 'capacity': '135 MW'},  # Central Delhi
        {'name': 'Yamuna Nagar TPS', 'lon': 77.2800, 'lat': 30.1000, 'capacity': '600 MW'},  # Haryana - slightly north
        {'name': 'Khedar TPS', 'lon': 77.2000, 'lat': 28.7000, 'capacity': '200 MW'},  # Near Delhi
        {'name': 'Badarpur TPS', 'lon': 77.3000, 'lat': 28.4800, 'capacity': '705 MW'},  # South Delhi
        {'name': 'NTPC Dadri Unit 2', 'lon': 77.5600, 'lat': 28.5600, 'capacity': '490 MW'},  # Near Dadri
        {'name': 'NTPC Badarpur', 'lon': 77.3100, 'lat': 28.4900, 'capacity': '705 MW'},  # South Delhi
        {'name': 'Faridabad TPS', 'lon': 77.3200, 'lat': 28.4200, 'capacity': '150 MW'},  # Faridabad
        {'name': 'Ghaziabad TPS', 'lon': 77.4200, 'lat': 28.6700, 'capacity': '100 MW'},  # Ghaziabad
    ],
    'gas': [
        {'name': 'Pragati Power Station', 'lon': 77.2800, 'lat': 28.5800, 'capacity': '1500 MW'},  # Active
        {'name': 'Bawana Gas Power Plant', 'lon': 77.0500, 'lat': 28.8000, 'capacity': '1500 MW'},  # Active
        {'name': 'Faridabad Gas Power Plant', 'lon': 77.3500, 'lat': 28.4000, 'capacity': '432 MW'},  # Active
        {'name': 'Gurgaon Gas Power Plant', 'lon': 77.1000, 'lat': 28.4000, 'capacity': '250 MW'},  # Near Delhi
        {'name': 'Ghaziabad Gas Power Plant', 'lon': 77.4500, 'lat': 28.6500, 'capacity': '200 MW'},  # Near Delhi
    ]
}

# Color and marker definitions for power plants (consistent across all frames)
POWER_PLANT_COLORS = {
    'coal': 'black',
    'gas': 'green'
}

POWER_PLANT_MARKERS = {
    'coal': 's',  # square
    'gas': '^',   # triangle
}

def add_power_plant_points(ax):
    """Add colorful point markers for major power plants with legend."""
    # Get map extent to filter plants within view
    extent = ax.get_extent()
    lon_min, lon_max, lat_min, lat_max = extent
    
    # Plot power plants within the map extent
    legend_elements = []
    plotted_types = set()
    
    for plant_type, plants in MAJOR_POWER_PLANTS.items():
        for plant in plants:
            # Check if plant is within map extent (with some buffer)
            if (lon_min - 0.5 <= plant['lon'] <= lon_max + 0.5 and 
                lat_min - 0.5 <= plant['lat'] <= lat_max + 0.5):
                
                # Use matplotlib named colors for absolute consistency
                if plant_type == 'coal':
                    plot_color = 'black'  # Matplotlib named color
                    marker = 's'  # square
                elif plant_type == 'gas':
                    plot_color = 'black'  # Matplotlib named color
                    marker = '^'  # triangle
                else:
                    continue
                
                # Plot with explicit named color - no transparency
                ax.plot(plant['lon'], plant['lat'], 
                       marker=marker, markersize=12, 
                       color=plot_color, markeredgecolor='white',
                       markeredgewidth=1.5, transform=ccrs.PlateCarree(),
                       zorder=12, alpha=1.0)
                
                # Add to legend if not already added - use same hex color
                if plant_type not in plotted_types:
                    legend_elements.append(
                        plt.Line2D([0], [0], marker=marker, color='w', 
                                  markerfacecolor=plot_color, markersize=10,
                                  markeredgecolor='white', markeredgewidth=1.5,
                                  label=f"{plant_type.title()} Power Plants")
                    )
                    plotted_types.add(plant_type)
    
    # Add legend if there are any power plants
    if legend_elements:
        ax.legend(handles=legend_elements, loc='upper left', 
                fontsize=9, framealpha=0.9, edgecolor='black')
    
    return legend_elements

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
    # Configure gridlines to avoid overlap with colorbar
    gl = ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--', dms=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = True
    gl.bottom_labels = True
    
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
        cbar = plt.colorbar(im, ax=ax, label=f"{pollutant_info['name']} ({pollutant_info['unit']})",
                    shrink=0.8, pad=0.05, aspect=30)
        cbar.ax.tick_params(labelsize=9)
        cbar.set_label(f"{pollutant_info['name']} ({pollutant_info['unit']})", fontsize=10)
    
    # Add Delhi ROI contour
    add_delhi_roi_contour(ax)
    
    # Add Delhi center marker
    ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'], 
           'r*', markersize=20, transform=ccrs.PlateCarree(), 
           label='Delhi Center', zorder=10)
    
    # Known sources removed - they were validation markers (power plants and industrial areas)
    
    ax.set_title(f"{pollutant_info['name']} - {month_str}", fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout(pad=2.0)
    
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
        # Configure gridlines to avoid overlap with colorbar
        gl = ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--', dms=True)
        gl.top_labels = False
        gl.right_labels = False
        gl.left_labels = True
        gl.bottom_labels = True
        
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
                # Position colorbar to avoid overlap with right-side labels
                cbar = plt.colorbar(im, ax=ax, label='Anomaly (mol/m²)',
                           shrink=0.6, pad=0.12, aspect=25)
                cbar.ax.tick_params(labelsize=8)
                cbar.set_label('Anomaly (mol/m²)', fontsize=9)
            
            # Add Delhi ROI contour
            add_delhi_roi_contour(ax)
            
            ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'],
                   'r*', markersize=15, transform=ccrs.PlateCarree(), zorder=10)
        
        ax.set_title(f"{season_name.capitalize()} Anomaly", fontsize=11, fontweight='bold', pad=10)
    
    plt.suptitle(f"{pollutant_info['name']} - Seasonal Anomalies (vs Annual Mean)",
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout(pad=2.5, h_pad=2.0, w_pad=2.0)
    
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
    
    # Get value range for consistent colormap (use percentiles to better show hotspots)
    all_values = composite.values
    all_values_clean = all_values[~np.isnan(all_values)]
    if len(all_values_clean) > 0:
        vmin = np.nanpercentile(all_values, 5)  # Use 5th percentile instead of min
        vmax = np.nanpercentile(all_values, 95)  # Use 95th percentile instead of max
    else:
        vmin = np.nanmin(all_values)
        vmax = np.nanmax(all_values)
    
    # Use a colormap that emphasizes hotspots (YlOrRd for better contrast)
    if pollutant_code in ['HCHO', 'SO2']:
        # Use a colormap that better shows clustering for these pollutants
        cmap = 'YlOrRd'  # Yellow-Orange-Red, good for showing hotspots
    else:
        cmap = 'viridis'
    
    # Initialize plot using pcolormesh instead of contourf to preserve local variations
    values = composite.isel(time=0).values
    if values.ndim > 2:
        values = values.squeeze()
    
    # Use pcolormesh for better preservation of hotspots (no interpolation)
    im = ax.pcolormesh(LON, LAT, values,
                      transform=ccrs.PlateCarree(),
                      cmap=cmap, shading='auto',
                      vmin=vmin, vmax=vmax, alpha=0.9)
    
    cbar = plt.colorbar(im, ax=ax, label=f"{pollutant_info['name']} ({pollutant_info['unit']})",
                       shrink=0.8, pad=0.05, aspect=30, extend='both')
    cbar.ax.tick_params(labelsize=9)
    cbar.set_label(f"{pollutant_info['name']} ({pollutant_info['unit']})", fontsize=10)
    
    # Add Delhi ROI contour
    add_delhi_roi_contour(ax)
    
    # Add power plant points with legend and get legend handles for consistent colors
    legend_handles = add_power_plant_points(ax)
    
    # Get extent bounds for filtering in animation
    lon_min, lon_max, lat_min, lat_max = extent
    
    # Remove Delhi center marker (as per previous request)
    
    title = ax.set_title(f"{pollutant_info['name']} - {composite.time.values[0]}",
                        fontsize=13, fontweight='bold', pad=20)
    
    def animate(frame):
        ax.clear()
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, alpha=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.5)
        gl = ax.gridlines(draw_labels=True, alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        
        values = composite.isel(time=frame).values
        if values.ndim > 2:
            values = values.squeeze()
        
        # Use pcolormesh for better preservation of hotspots (no interpolation)
        im = ax.pcolormesh(LON, LAT, values,
                          transform=ccrs.PlateCarree(),
                          cmap=cmap, shading='auto',
                          vmin=vmin, vmax=vmax, alpha=0.9)
        
        # Add Delhi ROI contour
        add_delhi_roi_contour(ax)
        
        # Add power plant points with consistent colors (black for coal, green for gas)
        # Plot power plants without recreating legend each frame
        for plant_type, plants in MAJOR_POWER_PLANTS.items():
            for plant in plants:
                # Check if plant is within map extent
                if (lon_min - 0.5 <= plant['lon'] <= lon_max + 0.5 and 
                    lat_min - 0.5 <= plant['lat'] <= lat_max + 0.5):
                    
                    # Use matplotlib named colors - EXACT SAME as initial plot
                    if plant_type == 'coal':
                        plot_color = 'black'  # Matplotlib named color
                        marker = 's'  # square
                    elif plant_type == 'gas':
                        plot_color = 'black'  # Matplotlib named color
                        marker = '^'  # triangle
                    else:
                        continue  # Skip unknown types
                    
                    ax.plot(plant['lon'], plant['lat'], 
                           marker=marker, markersize=12, 
                           color=plot_color, markeredgecolor='white',
                           markeredgewidth=1.5, transform=ccrs.PlateCarree(),
                           zorder=12, alpha=1.0)
        
        # Re-add legend with consistent handles (only if we have plants in view)
        # Use the same handles from initial plot to ensure color consistency
        if legend_handles and len(legend_handles) > 0:
            # Clear any existing legend first
            if ax.get_legend():
                ax.get_legend().remove()
            ax.legend(handles=legend_handles, loc='upper left', 
                    fontsize=9, framealpha=0.9, edgecolor='black')
        
        # Remove Delhi center marker (as per previous request)
        
        time_str = str(composite.time.values[frame])[:7]  # YYYY-MM
        ax.set_title(f"{pollutant_info['name']} - {time_str}",
                    fontsize=13, fontweight='bold', pad=20)
        
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
