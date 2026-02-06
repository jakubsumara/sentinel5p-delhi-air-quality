# Complete Analysis Workflow

This document describes the complete, reproducible workflow for the Sentinel-5P air pollution analysis project.

## Quick Start

### Option 1: Run Complete Pipeline (Recommended)

```bash
python run_analysis.py
```

This will run all steps automatically:
1. Setup verification
2. Data download (interactive)
3. Data processing
4. Analysis
5. Visualization

### Option 2: Run Individual Steps

```bash
# Step 1: Verify setup
python run_analysis.py --step setup

# Step 2: Download data
python run_analysis.py --step download

# Step 3: Process data
python run_analysis.py --step process

# Step 4: Run analysis
python run_analysis.py --step analyze

# Step 5: Generate visualizations
python run_analysis.py --step visualize
```

### Option 3: Use Jupyter Notebook

```bash
jupyter notebook notebooks/01_complete_analysis.ipynb
```

---

## Detailed Workflow

### Phase 1: Setup and Data Acquisition

#### 1.1 Environment Setup

```bash
# Create conda environment (recommended)
setup_conda_env.bat  # Windows
# or
./setup_conda_env.sh  # Linux/Mac

# Or use venv
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt
```

#### 1.2 Verify Setup

```bash
python scripts/setup_check.py
```

#### 1.3 Google Earth Engine Setup

```bash
python scripts/setup_gee.py
```

Follow the authentication flow in your browser.

#### 1.4 ERA5 Data Access Setup

1. Register at https://cds.climate.copernicus.eu/
2. Get API key from your profile
3. Create `~/.cdsapirc` file:

```ini
url: https://cds.climate.copernicus.eu/api
key: YOUR_UID:YOUR_API_KEY
```

Or use the helper script:
```bash
python scripts/fix_cds_config.py
```

---

### Phase 2: Data Download

#### 2.1 Download Sentinel-5P Data (Google Earth Engine)

```bash
python scripts/download_gee.py
```

**Note:** Files will be exported to Google Drive. Download them manually and place in `data/processed/`.

#### 2.2 Download ERA5 Wind Data

```bash
python scripts/download_era5.py
```

Select option 1 to download, then option 2 to process to daily averages.

---

### Phase 3: Data Processing

#### 3.1 Process ERA5 Data

```bash
python scripts/process_era5.py
```

This creates daily averaged wind data from hourly ERA5 files.

#### 3.2 Process Sentinel-5P Data

```bash
python scripts/process_sentinel5p.py
```

This will:
- Load GeoTIFF files from `data/processed/`
- Clip to Delhi ROI
- Create monthly composites
- Generate time series CSV files

**Expected outputs:**
- `data/processed/NO2_monthly_composite.nc`
- `data/processed/NO2_timeseries.csv`
- (Same for SO2, CO, HCHO)

---

### Phase 4: Analysis

#### 4.1 Trajectory Analysis

```bash
python scripts/trajectory_analysis.py
```

This classifies pollution as local vs. advected based on wind conditions.

**Outputs:**
- `data/processed/*_classified.csv` - Monthly data with regime classification
- `data/processed/*_severe_episodes.csv` - Dates of severe pollution episodes

#### 4.2 Hotspot Analysis

```bash
python scripts/hotspot_analysis.py
```

This identifies persistent pollution hotspots.

**Outputs:**
- `data/processed/*_hotspots.csv` - Coordinates of identified hotspots

---

### Phase 5: Visualization

#### 5.1 Time Series Plots

```bash
python scripts/visualize.py
```

**Outputs:**
- `outputs/time_series/*_timeseries.png` - Time series plots
- `outputs/time_series/*_regime_comparison.png` - Local vs. advected comparison

#### 5.2 Map Visualizations

```bash
python scripts/create_maps.py
```

**Outputs:**
- `outputs/maps/*_seasonal_anomaly.png` - Seasonal anomaly maps for each pollutant
- `outputs/animations/*_animation.gif` - 24-month temporal evolution animations with power plant locations

#### 5.3 Source Attribution Maps

```bash
python scripts/create_source_attribution.py
```

**Outputs:**
- `outputs/maps/source_attribution_*.png` - Seasonal back-trajectory maps (winter, summer, monsoon, post_monsoon)
- Shows averaged trajectories for advected pollution days with wind flow visualization

---

## File Structure After Complete Workflow

```
projSentinel/
├── data/
│   ├── era5/
│   │   ├── era5_wind_202201.nc          # Raw ERA5 (hourly)
│   │   ├── era5_wind_202201_daily.nc    # Processed (daily)
│   │   └── ... (25 months)
│   └── processed/
│       ├── Delhi_NO2_202201.tif         # Raw Sentinel-5P (from GEE)
│       ├── NO2_monthly_composite.nc     # Processed composite
│       ├── NO2_timeseries.csv           # Time series
│       ├── NO2_classified.csv           # With regime classification
│       ├── NO2_severe_episodes.csv      # Severe episodes
│       ├── NO2_hotspots.csv             # Hotspot locations
│       └── ... (same for SO2, CO, HCHO)
│
├── outputs/
│   ├── time_series/
│   │   ├── NO2_timeseries.png
│   │   ├── NO2_regime_comparison.png
│   │   └── ... (for all pollutants)
│   ├── maps/
│   │   ├── NO2_seasonal_anomaly.png
│   │   ├── source_attribution_winter.png
│   │   ├── source_attribution_summer.png
│   │   ├── source_attribution_monsoon.png
│   │   ├── source_attribution_post_monsoon.png
│   │   └── ... (seasonal anomalies for all pollutants)
│   ├── animations/
│   │   ├── NO2_animation.gif
│   │   └── ... (for all pollutants)
│   └── reports/
│       └── Interpretive_Note_Sentinel5P_Delhi.md
│
├── scripts/                              # All analysis scripts
├── notebooks/
│   └── 01_complete_analysis.ipynb       # Interactive notebook
├── run_analysis.py                       # Main workflow script
└── README.md
```

---

## Troubleshooting

### Data Not Found

**Problem:** Scripts report missing data files.

**Solution:**
1. Check that files are in the correct directories
2. Verify file naming matches expected patterns
3. Run `python run_analysis.py --step process` to regenerate processed files

### Google Earth Engine Authentication

**Problem:** `ee.Authenticate()` fails.

**Solution:**
1. Run `python scripts/setup_gee.py`
2. Follow browser authentication
3. Check that credentials are saved

### ERA5 Download Fails

**Problem:** 403 Forbidden error.

**Solution:**
1. Accept ERA5 license at https://cds.climate.copernicus.eu/
2. Verify `.cdsapirc` file format
3. Run `python scripts/fix_cds_config.py`

### Processing Errors

**Problem:** Scripts fail during processing.

**Solution:**
1. Check that input files exist and are readable
2. Verify Python environment has all packages
3. Check error messages for specific issues

---

## Reproducibility

### Version Control

All code is organized in the `scripts/` directory with clear dependencies on `config.py`.

### Data Dependencies

- **Sentinel-5P:** Downloaded from Google Earth Engine (reproducible via GEE scripts)
- **ERA5:** Downloaded from Copernicus CDS (requires API key, but data is consistent)

### Environment

- Python 3.11+ recommended
- All dependencies listed in `requirements.txt`
- Configuration in `config.py` (can be modified for different regions)

### Reproducing Results

1. Set up environment (see Phase 1)
2. Download data (see Phase 2)
3. Run `python run_analysis.py` (or individual steps)
4. Results will be in `outputs/` directory

---

## Next Steps

After completing the workflow:

1. **Review outputs:**
   - Check `outputs/reports/Interpretive_Note_Sentinel5P_Delhi.md`
   - Review visualizations in `outputs/`

2. **Customize analysis:**
   - Modify `config.py` for different regions or time periods
   - Adjust thresholds in analysis scripts

3. **Review results:**
   - Check seasonal patterns in anomaly maps
   - Review source attribution by season
   - Analyze time series trends

---

## Support

For issues or questions:
1. Check this workflow document
2. Review error messages carefully
3. Check individual script documentation
4. See `README.md` for general project information
