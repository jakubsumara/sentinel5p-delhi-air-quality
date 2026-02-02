# Google Earth Engine Setup Guide

## Quick Setup

### Step 1: Install Earth Engine API (if not already installed)
```bash
pip install earthengine-api
```

### Step 2: Authenticate
```bash
python scripts/setup_gee.py
```

This will:
- Open a browser window for Google authentication
- Save credentials for future use
- Test the connection

### Step 3: Verify Setup
```bash
python scripts/setup_gee.py check
```

## Manual Setup

### Authenticate Manually
```python
import ee
ee.Authenticate()  # Opens browser for authentication
ee.Initialize()     # Initialize Earth Engine
```

### Test Connection
```python
import ee
ee.Initialize()

# Test with Sentinel-5P
collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
count = collection.size().getInfo()
print(f"Found {count} images")
```

## Using the Scripts

### 1. Setup Script (`scripts/setup_gee.py`)
```bash
# Run setup
python scripts/setup_gee.py

# Check status
python scripts/setup_gee.py check
```

### 2. Download Script (`scripts/download_gee.py`)
```bash
python scripts/download_gee.py
```

This interactive script lets you:
- Download monthly composites for all pollutants
- Download specific pollutant data
- Get time series data

### 3. Helper Functions (`scripts/gee_helpers.py`)
Use these functions in your own scripts:
```python
from scripts.gee_helpers import (
    initialize_gee,
    get_delhi_roi,
    get_sentinel5p_collection,
    create_monthly_composite,
    calculate_area_average
)

# Initialize
initialize_gee()

# Get collection
collection = get_sentinel5p_collection('NO2', '2024-01-01', '2024-01-31')

# Create composite
composite = create_monthly_composite(collection, 'NO2_column_number_density', 
                                     '2024-01-01', '2024-01-31')
```

## Sentinel-5P Collections in Google Earth Engine

Available collections:
- **NO2**: `COPERNICUS/S5P/OFFL/L3_NO2`
  - Band: `NO2_column_number_density`
- **SO2**: `COPERNICUS/S5P/OFFL/L3_SO2`
  - Band: `SO2_column_number_density`
- **CO**: `COPERNICUS/S5P/OFFL/L3_CO`
  - Band: `CO_column_number_density`
- **HCHO**: `COPERNICUS/S5P/OFFL/L3_HCHO`
  - Band: `HCHO_column_number_density`

## Exporting Data

### Export to Google Drive
```python
import ee
ee.Initialize()

# Get your image
image = ee.Image('...')

# Export
task = ee.batch.Export.image.toDrive(
    image=image,
    description='my_export',
    folder='Sentinel5P_Delhi',
    fileNamePrefix='delhi_no2',
    scale=1000,  # 1km resolution
    region=roi,
    fileFormat='GeoTIFF'
)

task.start()
```

### Check Export Status
Visit: https://code.earthengine.google.com/tasks

Or in Python:
```python
import time

# Wait for task to complete
while task.active():
    print(f"Task {task.id} is still running...")
    time.sleep(10)

print("Task completed!")
```

## Advantages of Google Earth Engine

1. **No Local Storage Needed**: Process data in the cloud
2. **Fast Processing**: Google's servers handle computation
3. **Large Dataset Access**: Access entire Sentinel-5P archive
4. **Free**: No cost for reasonable usage
5. **Pre-processed**: Level-3 data is already gridded

## Limitations

1. **Export Limits**: 
   - 10,000 tasks per day
   - 2GB per export (can request more)
2. **Processing Time**: Large exports can take hours
3. **Internet Required**: Need connection to use
4. **Learning Curve**: GEE API is different from standard Python

## Troubleshooting

### "Please authenticate" Error
```bash
python scripts/setup_gee.py
```

### "Quota exceeded" Error
- Wait 24 hours for quota reset
- Reduce export size
- Use smaller date ranges

### Export Taking Too Long
- Reduce resolution (increase `scale` parameter)
- Reduce region size
- Export in smaller time chunks

### Can't Find Collection
- Check collection name spelling
- Verify collection exists: https://developers.google.com/earth-engine/datasets
- Some collections may be deprecated

## Next Steps

After setting up Google Earth Engine:

1. ✅ Authenticate and verify setup
2. Run download script: `python scripts/download_gee.py`
3. Or use in notebooks: `notebooks/01_data_download.ipynb`
4. Check exports in Google Drive
5. Download exported files to `data/processed/`

## Resources

- [Earth Engine Documentation](https://developers.google.com/earth-engine)
- [Sentinel-5P in GEE](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_NO2)
- [Earth Engine Code Editor](https://code.earthengine.google.com/)
- [Earth Engine Tasks](https://code.earthengine.google.com/tasks)
