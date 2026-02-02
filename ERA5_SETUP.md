# ERA5 Wind Data Setup Guide

## Overview

ERA5 is ECMWF's reanalysis dataset providing global atmospheric data including wind components. We need u-wind and v-wind data for trajectory analysis to distinguish local vs advected pollution.

## Setup Methods

### Method 1: Copernicus Climate Data Store (CDS) API (Recommended)

#### Step 1: Register and Get API Key

1. **Register at CDS:**
   - Go to: https://cds.climate.copernicus.eu/
   - Create an account (free)

2. **Get API Key:**
   - Log in and go to: https://cds.climate.copernicus.eu/#!/home
   - Click "Your profile" (top right)
   - Click "API key"
   - Copy your UID and API key

#### Step 2: Create CDS API Configuration File

Create a file `~/.cdsapirc` (or `C:\Users\YourName\.cdsapirc` on Windows) with:

```
url: https://cds.climate.copernicus.eu/api
key: YOUR_API_KEY
```

**Important:** The key should NOT include the UID prefix anymore!

**Example:**
```
url: https://cds.climate.copernicus.eu/api
key: abcdef123456-7890-abcdef123456
```

**Or use the helper script:**
```bash
python scripts/fix_cds_config.py
```

#### Step 3: Install/Update CDS API Client

```bash
pip install --upgrade cdsapi
```

Make sure you have the latest version to use the updated API endpoint.

#### Step 4: Download Data

```bash
python scripts/download_era5.py
```

### Method 2: Google Earth Engine (Alternative)

**Note:** ERA5 may not be fully available in Google Earth Engine. Check availability first.

```bash
python scripts/download_era5_gee.py
```

## Data Specifications

- **Variables:** u-component of wind, v-component of wind
- **Pressure Level:** 850 hPa (boundary layer, ~1.5 km altitude)
- **Resolution:** 0.25° × 0.25° (~25 km)
- **Temporal Resolution:** Hourly (we'll average to daily)
- **Region:** Delhi NCR + buffer (for trajectory analysis)

## Download Process

### Automatic Download

The script downloads data month by month:

```bash
python scripts/download_era5.py
# Choose option 1: Download ERA5 wind data
```

### Manual Download (via CDS Website)

1. Go to: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels
2. Select:
   - Variables: u-component of wind, v-component of wind
   - Pressure level: 850 hPa
   - Year, month, day, time
   - Area: [30, 74, 26, 80] (North, West, South, East)
   - Format: NetCDF
3. Submit request and download

## Processing Downloaded Data

After downloading, process to daily averages:

```bash
python scripts/download_era5.py
# Choose option 2: Process downloaded files
```

This will:
- Calculate daily averages from hourly data
- Calculate wind speed and direction
- Save processed files as `*_daily.nc`

## File Structure

```
data/era5/
├── era5_wind_202201.nc      # January 2022 (hourly)
├── era5_wind_202201_daily.nc # January 2022 (daily average)
├── era5_wind_202202.nc
└── ...
```

## Using the Data

### Load in Python

```python
import xarray as xr

# Load daily average
ds = xr.open_dataset('data/era5/era5_wind_202201_daily.nc')

# Access wind components
u_wind = ds['u']  # u-component (m/s)
v_wind = ds['v']  # v-component (m/s)
wind_speed = ds['wind_speed']  # Calculated speed
wind_direction = ds['wind_direction']  # Calculated direction
```

### Calculate Trajectories

```python
# Simple back-trajectory calculation
# (Full implementation in trajectory analysis script)

def calculate_back_trajectory(lon, lat, start_time, hours=72):
    """
    Calculate back-trajectory from a point.
    
    Parameters:
    -----------
    lon, lat : float
        Starting point coordinates
    start_time : datetime
        Starting time
    hours : int
        Number of hours to go back
    """
    # Load wind data for the time period
    # Interpolate wind at trajectory points
    # Integrate backward in time
    # Return trajectory path
    pass
```

## Troubleshooting

### "CDS API not set up" Error

1. Check that `~/.cdsapirc` file exists
2. Verify API key format: `UID:API_KEY`
3. Make sure you're logged in at CDS website

### Download Fails

- Check internet connection
- Verify API key is correct
- Try downloading smaller date ranges
- Check CDS service status: https://cds.climate.copernicus.eu/

### Files Too Large

- Each month is ~50-100 MB
- 24 months = ~1-2 GB
- Consider downloading only specific months if storage is limited
- Use daily averages to reduce size

### Processing Errors

- Make sure `netcdf4` and `xarray` are installed
- Check file integrity (try opening with `xr.open_dataset()`)
- Verify files are complete (not corrupted during download)

## Storage Considerations

- **Raw hourly data:** ~50-100 MB per month
- **Daily averages:** ~5-10 MB per month
- **24 months total:** ~1-2 GB (hourly) or ~200 MB (daily)

**Recommendation:** Keep daily averages, delete hourly files if storage is limited.

## Next Steps

After downloading ERA5 data:

1. ✅ Download ERA5 wind data
2. Process to daily averages
3. Use in trajectory analysis (todo #5)
4. Classify pollution as local vs advected

## Resources

- [CDS API Documentation](https://cds.climate.copernicus.eu/api-how-to)
- [ERA5 Dataset](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels)
- [ERA5 Documentation](https://confluence.ecmwf.int/display/CKB/ERA5)
