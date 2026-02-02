"""
Visualization Script
Creates maps, time-series plots, and animations for the project.
"""

import os
import sys
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def setup_map(ax, extent=None):
    """Set up a map with cartopy."""
    if extent is None:
        extent = [
            config.DELHI_ROI['lon_min'] - 0.5,
            config.DELHI_ROI['lon_max'] + 0.5,
            config.DELHI_ROI['lat_min'] - 0.5,
            config.DELHI_ROI['lat_max'] + 0.5
        ]
    
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.RIVERS, linewidth=0.3, alpha=0.5)
    ax.gridlines(draw_labels=True, alpha=0.5)
    
    return ax

def plot_monthly_map(pollutant_code, month_data, output_dir='outputs/maps'):
    """Plot a single monthly map."""
    os.makedirs(output_dir, exist_ok=True)
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    
    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    setup_map(ax)
    
    # Plot data
    if hasattr(month_data, 'plot'):
        im = month_data.plot(ax=ax, transform=ccrs.PlateCarree(), 
                            cmap='viridis', add_colorbar=True)
    else:
        # Handle different data structures
        if hasattr(month_data, 'values'):
            lon = month_data.lon.values if 'lon' in month_data.coords else month_data.x.values
            lat = month_data.lat.values if 'lat' in month_data.coords else month_data.y.values
            values = month_data.values
            
            im = ax.contourf(lon, lat, values, transform=ccrs.PlateCarree(), 
                           cmap='viridis', levels=20)
            plt.colorbar(im, ax=ax, label=f"{pollutant_info['name']} ({pollutant_info['unit']})")
    
    ax.set_title(f"{pollutant_info['name']} - {month_data.time.values if 'time' in month_data.coords else 'Monthly Mean'}")
    
    # Add Delhi center marker
    ax.plot(config.DELHI_CENTER['lon'], config.DELHI_CENTER['lat'], 
           'r*', markersize=15, transform=ccrs.PlateCarree(), label='Delhi Center')
    
    plt.tight_layout()
    return fig, ax

def create_time_series_plot(pollutant_code, output_dir='outputs/time_series'):
    """Create time series plot with seasonal decomposition."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Load time series
    ts_file = f"data/processed/{pollutant_code}_timeseries.csv"
    if not os.path.exists(ts_file):
        print(f"[WARNING] Time series not found: {ts_file}")
        return
    
    df = pd.read_csv(ts_file, index_col=0, parse_dates=True)
    
    # Load classified data if available
    classified_file = f"data/processed/{pollutant_code}_classified.csv"
    if os.path.exists(classified_file):
        classified = pd.read_csv(classified_file, index_col=0, parse_dates=True)
    else:
        classified = None
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Get the value column (might be named 'value' or first column)
    if 'value' in df.columns:
        value_col = 'value'
    else:
        value_col = df.columns[0]
    
    # Filter out NaN values for plotting
    plot_df = df.dropna(subset=[value_col])
    
    if plot_df.empty:
        print(f"[WARNING] No valid data to plot for {pollutant_code}")
        return
    
    # Plot 1: Time series
    ax1 = axes[0]
    ax1.plot(plot_df.index, plot_df[value_col], 'b-', linewidth=2, label='Monthly Average', marker='o', markersize=4)
    ax1.set_ylabel(f"{pollutant_info['name']} ({pollutant_info['unit']})")
    ax1.set_title(f"{pollutant_info['name']} - 24 Month Time Series")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Seasonal decomposition
    ax2 = axes[1]
    plot_df['month'] = plot_df.index.month
    seasonal_means = plot_df.groupby('month')[value_col].mean()
    ax2.bar(range(1, 13), [seasonal_means.get(m, 0) for m in range(1, 13)], color='coral', alpha=0.7)
    ax2.set_xlabel('Month')
    ax2.set_ylabel(f"{pollutant_info['name']} ({pollutant_info['unit']})")
    ax2.set_title('Seasonal Pattern')
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, f"{pollutant_code}_timeseries.png")
    plt.savefig(output_file, dpi=config.VISUALIZATION['figure_dpi'], 
                format=config.VISUALIZATION['figure_format'])
    print(f"[OK] Saved time series plot: {output_file}")
    plt.close()

def create_regime_comparison_plot(pollutant_code, output_dir='outputs/time_series'):
    """Create plot comparing local vs advected regimes."""
    os.makedirs(output_dir, exist_ok=True)
    
    classified_file = f"data/processed/{pollutant_code}_classified.csv"
    if not os.path.exists(classified_file):
        print(f"[WARNING] Classified data not found: {classified_file}")
        return
    
    df = pd.read_csv(classified_file, index_col=0, parse_dates=True)
    
    if 'is_local' not in df.columns or 'value' not in df.columns:
        print(f"[WARNING] Required columns not found in {classified_file}")
        return
    
    pollutant_info = config.POLLUTANTS[pollutant_code]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Filter out NaN values
    df_clean = df.dropna(subset=['value'])
    
    if df_clean.empty:
        print(f"[WARNING] No valid data to plot for {pollutant_code}")
        return
    
    # Plot local vs advected
    local_data = df_clean[df_clean['is_local'] == True]
    advected_data = df_clean[df_clean['is_advected'] == True]
    
    if not local_data.empty:
        ax.scatter(local_data.index, local_data['value'], 
                  color='red', alpha=0.7, label=f'Local (n={len(local_data)})', 
                  s=80, marker='o', edgecolors='darkred', linewidths=1.5)
        # Add mean line for local
        ax.axhline(y=local_data['value'].mean(), color='red', 
                  linestyle='--', alpha=0.5, linewidth=2, label=f'Local mean: {local_data["value"].mean():.6f}')
    
    if not advected_data.empty:
        ax.scatter(advected_data.index, advected_data['value'], 
                  color='blue', alpha=0.7, label=f'Advected (n={len(advected_data)})', 
                  s=80, marker='s', edgecolors='darkblue', linewidths=1.5)
        # Add mean line for advected
        ax.axhline(y=advected_data['value'].mean(), color='blue', 
                  linestyle='--', alpha=0.5, linewidth=2, label=f'Advected mean: {advected_data["value"].mean():.6f}')
    
    # Also plot a line connecting all points
    ax.plot(df_clean.index, df_clean['value'], 'k-', alpha=0.2, linewidth=1, zorder=0)
    
    # Add statistics text box
    if not local_data.empty and not advected_data.empty:
        stats_text = f'Local: μ={local_data["value"].mean():.6f}, σ={local_data["value"].std():.6f}\n'
        stats_text += f'Advected: μ={advected_data["value"].mean():.6f}, σ={advected_data["value"].std():.6f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_ylabel(f"{pollutant_info['name']} ({pollutant_info['unit']})")
    ax.set_title(f"{pollutant_info['name']} - Local vs Advected Regimes")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, f"{pollutant_code}_regime_comparison.png")
    plt.savefig(output_file, dpi=config.VISUALIZATION['figure_dpi'],
                format=config.VISUALIZATION['figure_format'])
    print(f"[OK] Saved regime comparison: {output_file}")
    plt.close()

def main():
    """Main function."""
    print("="*60)
    print("Creating Visualizations")
    print("="*60)
    
    pollutants = ['NO2', 'SO2', 'CO', 'HCHO']
    
    for code in pollutants:
        print(f"\n{'='*60}")
        print(f"Visualizing {code}")
        print(f"{'='*60}")
        
        # Create time series plots
        create_time_series_plot(code)
        
        # Create regime comparison
        create_regime_comparison_plot(code)
    
    print("\n" + "="*60)
    print("[OK] Visualization complete!")
    print("="*60)
    print("\nOutputs saved in:")
    print("  - outputs/time_series/ (time series plots)")
    print("  - outputs/maps/ (map visualizations)")

if __name__ == "__main__":
    main()
