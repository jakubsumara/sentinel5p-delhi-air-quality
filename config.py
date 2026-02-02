"""
Configuration file for Sentinel-5P Delhi Air Pollution Project
"""

# Delhi NCR Region of Interest (ROI)
# Format: [min_lon, min_lat, max_lon, max_lat]
DELHI_ROI = {
    'lon_min': 76.5,
    'lon_max': 78.0,
    'lat_min': 28.0,
    'lat_max': 29.0
}

# Delhi center coordinates
DELHI_CENTER = {
    'lon': 77.2090,
    'lat': 28.6139
}

# Time period (24 months)
# Update these dates to cover the last 24 months
START_DATE = '2022-01-01'  # Adjust as needed
END_DATE = '2024-01-01'    # Adjust as needed

# Pollutants to analyze
POLLUTANTS = {
    'NO2': {
        'name': 'Nitrogen Dioxide',
        'unit': 'mol/m²',
        'description': 'Traffic/industrial emissions proxy',
        'gee_collection': 'COPERNICUS/S5P/OFFL/L3_NO2',
        'gee_band': 'NO2_column_number_density'
    },
    'SO2': {
        'name': 'Sulfur Dioxide',
        'unit': 'mol/m²',
        'description': 'Power plants proxy',
        'gee_collection': 'COPERNICUS/S5P/OFFL/L3_SO2',
        'gee_band': 'SO2_column_number_density'
    },
    'CO': {
        'name': 'Carbon Monoxide',
        'unit': 'mol/m²',
        'description': 'Biomass burning proxy',
        'gee_collection': 'COPERNICUS/S5P/OFFL/L3_CO',
        'gee_band': 'CO_column_number_density'
    },
    'HCHO': {
        'name': 'Formaldehyde',
        'unit': 'mol/m²',
        'description': 'Secondary pollution chemistry proxy',
        'gee_collection': 'COPERNICUS/S5P/OFFL/L3_HCHO',
        'gee_band': 'tropospheric_HCHO_column_number_density'  # Correct band name in GEE
    }
}

# Data processing settings
PROCESSING = {
    'grid_resolution': 0.01,  # degrees (approximately 1 km)
    'temporal_resolution': 'monthly',  # 'weekly' or 'monthly'
    'quality_threshold': 0.5,  # Minimum quality flag value (0-1)
    'cloud_fraction_max': 0.3,  # Maximum cloud fraction (0-1)
}

# ERA5 wind data settings
ERA5 = {
    'pressure_level': 850,  # hPa (850 hPa is typical for boundary layer)
    'variables': ['u_component_of_wind', 'v_component_of_wind'],
    'grid_resolution': 0.25,  # degrees
}

# Visualization settings
VISUALIZATION = {
    'figure_dpi': 300,
    'figure_format': 'png',
    'colormap': 'viridis',  # Scientific colormap
    'animation_fps': 2,  # Frames per second for animations
}

# Output directories
PATHS = {
    'data_raw': 'data/raw',
    'data_processed': 'data/processed',
    'data_era5': 'data/era5',
    'outputs_maps': 'outputs/maps',
    'outputs_animations': 'outputs/animations',
    'outputs_timeseries': 'outputs/time_series',
    'outputs_reports': 'outputs/reports',
}

# Known pollution sources in Delhi region (for validation)
KNOWN_SOURCES = {
    'power_plants': [
        {'name': 'Badarpur TPS', 'lon': 77.3083, 'lat': 28.5014},
        {'name': 'Rajghat TPS', 'lon': 77.2300, 'lat': 28.6400},
    ],
    'industrial_areas': [
        {'name': 'Okhla Industrial Area', 'lon': 77.2833, 'lat': 28.5500},
        {'name': 'Noida Industrial Area', 'lon': 77.3167, 'lat': 28.5667},
    ],
    'crop_burning_regions': [
        {'name': 'Punjab', 'lon': 75.3412, 'lat': 30.0668},
        {'name': 'Haryana', 'lon': 76.0856, 'lat': 29.0588},
    ]
}

# Seasonal definitions (for Delhi)
SEASONS = {
    'winter': ['12', '01', '02'],  # Dec, Jan, Feb
    'summer': ['03', '04', '05'],  # Mar, Apr, May
    'monsoon': ['06', '07', '08', '09'],  # Jun, Jul, Aug, Sep
    'post_monsoon': ['10', '11'],  # Oct, Nov (includes crop burning)
}
