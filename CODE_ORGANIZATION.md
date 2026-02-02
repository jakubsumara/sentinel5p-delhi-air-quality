# Code Organization

This document describes the organization of code in this project for reproducibility and clarity.

## Project Structure

```
projSentinel/
├── run_analysis.py              # Main entry point - runs complete pipeline
├── config.py                    # Centralized configuration
├── requirements.txt             # Python dependencies
│
├── scripts/                     # All analysis scripts
│   ├── __init__.py              # Package initialization
│   │
│   ├── setup_check.py           # Environment verification
│   ├── setup_gee.py             # Google Earth Engine authentication
│   │
│   ├── download_gee.py          # Download Sentinel-5P from GEE
│   ├── download_era5.py         # Download ERA5 wind data
│   ├── download_era5_gee.py     # Alternative: ERA5 from GEE
│   ├── download_hcho.py         # HCHO-specific download
│   ├── gee_helpers.py           # GEE helper functions
│   ├── fix_cds_config.py        # Fix CDS API configuration
│   │
│   ├── process_era5.py          # Process ERA5 to daily averages
│   ├── process_sentinel5p.py    # Process Sentinel-5P composites
│   │
│   ├── trajectory_analysis.py   # Local vs. advected classification
│   ├── hotspot_analysis.py      # Identify pollution hotspots
│   │
│   ├── visualize.py             # Time series plots
│   ├── create_maps.py           # Map visualizations
│   └── create_source_attribution.py  # Source attribution maps
│
├── notebooks/
│   └── 01_complete_analysis.ipynb  # Interactive workflow notebook
│
├── data/                        # Data directory (not in git)
│   ├── era5/                    # ERA5 wind data
│   └── processed/               # Processed Sentinel-5P data
│
├── outputs/                     # Analysis outputs
│   ├── time_series/             # Time series plots
│   ├── maps/                    # Map visualizations
│   ├── animations/               # Animation GIFs
│   └── reports/                  # Reports and documentation
│
└── Documentation/
    ├── README.md                # Main project documentation
    ├── WORKFLOW.md              # Detailed workflow guide
    ├── CODE_ORGANIZATION.md     # This file
    ├── ENVIRONMENT_SETUP.md     # Environment setup guide
    ├── GEE_SETUP.md            # Google Earth Engine setup
    ├── ERA5_SETUP.md           # ERA5 data access setup
    └── EXPLANATION_CLASSIFICATION.md  # Classification methodology
```

## Script Categories

### 1. Setup Scripts
- **`setup_check.py`**: Verifies all required packages are installed
- **`setup_gee.py`**: Handles Google Earth Engine authentication

### 2. Data Download Scripts
- **`download_gee.py`**: Downloads Sentinel-5P data from Google Earth Engine
- **`download_era5.py`**: Downloads ERA5 wind data from Copernicus CDS
- **`download_era5_gee.py`**: Alternative ERA5 download from GEE
- **`download_hcho.py`**: HCHO-specific download script
- **`gee_helpers.py`**: Helper functions for GEE operations
- **`fix_cds_config.py`**: Fixes CDS API configuration file

### 3. Data Processing Scripts
- **`process_era5.py`**: Converts hourly ERA5 data to daily averages
- **`process_sentinel5p.py`**: Processes GeoTIFF files into monthly composites

### 4. Analysis Scripts
- **`trajectory_analysis.py`**: Classifies pollution as local vs. advected
- **`hotspot_analysis.py`**: Identifies persistent pollution hotspots

### 5. Visualization Scripts
- **`visualize.py`**: Creates time series plots and regime comparisons
- **`create_maps.py`**: Generates map visualizations and animations
- **`create_source_attribution.py`**: Creates source attribution maps

## Main Entry Point

### `run_analysis.py`

The main entry point for running the complete analysis pipeline.

**Usage:**
```bash
# Run all steps
python run_analysis.py

# Run specific step
python run_analysis.py --step process

# Process specific pollutant
python run_analysis.py --step process --pollutant NO2
```

**Steps:**
1. `setup` - Verify environment
2. `download` - Download data
3. `process` - Process raw data
4. `analyze` - Run analysis
5. `visualize` - Generate visualizations
6. `all` - Run all steps (default)

## Configuration

### `config.py`

Centralized configuration file containing:
- Delhi ROI boundaries
- Time period settings
- Pollutant definitions
- Processing parameters
- Visualization settings
- File paths

**Modifying for different regions:**
1. Update `DELHI_ROI` dictionary
2. Update `DELHI_CENTER` coordinates
3. Adjust `KNOWN_SOURCES` if needed
4. Update time period if needed

## Data Flow

```
Raw Data
  ↓
[download_gee.py, download_era5.py]
  ↓
data/era5/*.nc, data/processed/*.tif
  ↓
[process_era5.py, process_sentinel5p.py]
  ↓
data/processed/*_monthly_composite.nc
data/processed/*_timeseries.csv
  ↓
[trajectory_analysis.py, hotspot_analysis.py]
  ↓
data/processed/*_classified.csv
data/processed/*_hotspots.csv
  ↓
[visualize.py, create_maps.py, create_source_attribution.py]
  ↓
outputs/
```

## Reproducibility

### Version Control

All code is version-controlled. Data files are excluded via `.gitignore`.

### Dependencies

All Python dependencies are listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Configuration

All configuration is in `config.py` - no hardcoded values in scripts.

### Data Access

- **Sentinel-5P**: Via Google Earth Engine (requires authentication)
- **ERA5**: Via Copernicus CDS API (requires API key)

Both require one-time setup but are reproducible.

## Running Individual Scripts

All scripts can be run independently:

```bash
# Setup
python scripts/setup_check.py
python scripts/setup_gee.py

# Download
python scripts/download_gee.py
python scripts/download_era5.py

# Process
python scripts/process_era5.py
python scripts/process_sentinel5p.py

# Analyze
python scripts/trajectory_analysis.py
python scripts/hotspot_analysis.py

# Visualize
python scripts/visualize.py
python scripts/create_maps.py
python scripts/create_source_attribution.py
```

## Jupyter Notebook

### `notebooks/01_complete_analysis.ipynb`

Interactive notebook for exploratory analysis:
- Data loading and exploration
- Quick visualizations
- Summary statistics
- Key findings

**Usage:**
```bash
jupyter notebook notebooks/01_complete_analysis.ipynb
```

## Best Practices

### 1. Use Main Entry Point
Prefer `run_analysis.py` over running scripts individually for reproducibility.

### 2. Check Data First
Always verify data availability before running analysis:
```bash
python run_analysis.py --step setup
```

### 3. Process Incrementally
Run steps one at a time to catch errors early:
```bash
python run_analysis.py --step process
python run_analysis.py --step analyze
```

### 4. Review Outputs
Check `outputs/` directory after each step to verify results.

### 5. Modify Config
Change `config.py` for different regions/time periods rather than editing scripts.

## Troubleshooting

### Script Not Found
Make sure you're in the project root directory:
```bash
cd /path/to/projSentinel
python run_analysis.py
```

### Import Errors
Ensure project root is in Python path (handled automatically by `run_analysis.py`).

### Data Not Found
Check that data files are in correct directories:
- ERA5: `data/era5/`
- Sentinel-5P: `data/processed/`

### Configuration Issues
Verify `config.py` settings match your data and region.

## Documentation

- **README.md**: Project overview and quick start
- **WORKFLOW.md**: Detailed workflow instructions
- **CODE_ORGANIZATION.md**: This file
- **ENVIRONMENT_SETUP.md**: Environment setup guide
- **GEE_SETUP.md**: Google Earth Engine setup
- **ERA5_SETUP.md**: ERA5 data access setup
- **EXPLANATION_CLASSIFICATION.md**: Classification methodology

## Contributing

When adding new scripts:
1. Place in appropriate category in `scripts/`
2. Add docstring with description
3. Use `config.py` for configuration
4. Update this document if needed
5. Test with `run_analysis.py`
