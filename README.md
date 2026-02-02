# Sentinel-5P Air Pollution Dynamics over Delhi NCR

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Project Overview

This project analyzes **24 months** of Sentinel-5P TROPOMI satellite data (January 2022 - January 2024) to study air pollution dynamics over Delhi NCR, focusing on four key pollutants:

- **NO₂** (Nitrogen Dioxide) - traffic/industrial emissions
- **SO₂** (Sulfur Dioxide) - power plants
- **CO** (Carbon Monoxide) - biomass burning
- **HCHO** (Formaldehyde) - secondary pollution chemistry

The analysis combines satellite data with ERA5 reanalysis wind data to distinguish **locally generated pollution** from **transported pollution**, providing insights for air quality management.

## 🎯 Key Findings

- **62.5% of time:** Local pollution dominant (low wind conditions)
- **37.5% of time:** Regional transport dominant (high wind conditions)
- **Strong seasonal patterns:** Winter (local sources), Post-monsoon (crop burning)
- **Source attribution:** Northwest (Punjab/Haryana crop burning), West (industrial regions)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/sentinel5p-delhi-air-quality.git
cd sentinel5p-delhi-air-quality
```

### 2. Set Up Environment

**Option A: Conda (Recommended)**
```bash
# Windows
setup_conda_env.bat

# Linux/Mac
chmod +x setup_conda_env.sh
./setup_conda_env.sh
```

**Option B: Python venv**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Complete Analysis

```bash
# Run all steps
python run_analysis.py

# Or run individual steps
python run_analysis.py --step setup      # Verify environment
python run_analysis.py --step download   # Download data
python run_analysis.py --step process     # Process data
python run_analysis.py --step analyze    # Run analysis
python run_analysis.py --step visualize  # Generate visualizations
```

See [WORKFLOW.md](WORKFLOW.md) for detailed instructions.

## 📁 Project Structure

```
projSentinel/
├── run_analysis.py              # Main workflow script
├── config.py                    # Centralized configuration
├── requirements.txt             # Python dependencies
│
├── scripts/                      # Analysis scripts
│   ├── setup_check.py           # Environment verification
│   ├── setup_gee.py             # Google Earth Engine setup
│   ├── download_gee.py          # Download Sentinel-5P data
│   ├── download_era5.py         # Download ERA5 wind data
│   ├── process_era5.py           # Process ERA5 data
│   ├── process_sentinel5p.py     # Process Sentinel-5P data
│   ├── trajectory_analysis.py   # Local vs. advected classification
│   ├── hotspot_analysis.py      # Hotspot detection
│   ├── visualize.py             # Time series plots
│   ├── create_maps.py           # Map visualizations
│   └── create_source_attribution.py  # Source attribution maps
│
├── notebooks/
│   └── 01_complete_analysis.ipynb  # Interactive workflow
│
├── outputs/                      # Analysis outputs
│   ├── maps/                     # Map visualizations
│   ├── animations/               # Temporal animations
│   ├── time_series/              # Time series plots
│   ├── reports/                   # Reports and documentation
│   └── presentation/              # Presentation slides
│
└── data/                         # Data directory (not in git)
    ├── era5/                     # ERA5 wind data
    └── processed/                # Processed Sentinel-5P data
```

## 📊 Deliverables

### 1. Gridded 24-Month Maps and Animations
- Monthly maps for all 4 pollutants
- Seasonal anomaly maps highlighting winter smog and post-harvest burning
- 24-month animations showing temporal evolution

**Location:** `outputs/maps/`, `outputs/animations/`

### 2. Time-Series Plots with Regime Decomposition
- Area-averaged concentrations for each pollutant
- Decomposed by season and "local" vs "advected" regimes
- Statistical summaries included

**Location:** `outputs/time_series/`

### 3. Source-Region Attribution Maps
- Back-trajectory analysis for severe episodes
- Upwind origin zones (Punjab/Haryana crop burning, industrial regions)
- Transport pathways visualization

**Location:** `outputs/maps/*_source_attribution.png`

### 4. Interpretive Note
- Sentinel-5P strengths and limitations
- Column vs. surface concentration issues
- Impact of cloud screening and overpass time
- Recommendations for Delhi air quality studies

**Location:** `outputs/reports/Interpretive_Note_Sentinel5P_Delhi.md`

## 🔧 Setup Requirements

### Google Earth Engine (For Sentinel-5P Data)

1. Register at [Google Earth Engine](https://earthengine.google.com/)
2. Authenticate:
   ```bash
   python scripts/setup_gee.py
   ```
3. See [GEE_SETUP.md](GEE_SETUP.md) for details

### Copernicus CDS (For ERA5 Wind Data)

1. Register at [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
2. Accept ERA5 license
3. Get API key from your profile
4. Create `~/.cdsapirc` file:
   ```ini
   url: https://cds.climate.copernicus.eu/api
   key: YOUR_UID:YOUR_API_KEY
   ```
5. See [ERA5_SETUP.md](ERA5_SETUP.md) for details

## 📖 Documentation

- **[WORKFLOW.md](WORKFLOW.md)** - Complete workflow guide
- **[CODE_ORGANIZATION.md](CODE_ORGANIZATION.md)** - Code structure and organization
- **[ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)** - Detailed environment setup
- **[GEE_SETUP.md](GEE_SETUP.md)** - Google Earth Engine setup
- **[ERA5_SETUP.md](ERA5_SETUP.md)** - ERA5 data access setup
- **[EXPLANATION_CLASSIFICATION.md](EXPLANATION_CLASSIFICATION.md)** - Classification methodology

## 🎤 Presentation

A 5-minute presentation covering key findings is available in `outputs/presentation/`:
- 7 slides (PNG format)
- Complete outline with timing guide
- Ready for YouTube recording

## 📈 Results Summary

### Pollution Regimes
- **Local (62.5%):** Low wind conditions, pollution accumulates locally
- **Advected (37.5%):** High wind conditions, pollution transported from surrounding regions

### Seasonal Patterns
- **Winter (Dec-Feb):** Elevated NO₂, SO₂ from heating and power generation
- **Post-Monsoon (Oct-Nov):** Peak CO, HCHO from crop residue burning
- **Summer (Mar-May):** Moderate levels with regional transport
- **Monsoon (Jun-Sep):** Limited data due to cloud cover

### Source Attribution
- **Northwest:** Punjab/Haryana crop burning regions
- **West:** Industrial areas and power plants
- **Local:** Delhi's own emissions during calm conditions

## 🛠️ Technologies Used

- **Python 3.11+**
- **xarray, rioxarray** - Geospatial data processing
- **pandas, numpy** - Data analysis
- **matplotlib, cartopy** - Visualization
- **Google Earth Engine API** - Cloud-based data processing
- **Copernicus CDS API** - ERA5 reanalysis data

## 📝 Citation

If you use this project, please cite:

```bibtex
@misc{sentinel5p-delhi-air-quality,
  title={Sentinel-5P Air Pollution Dynamics over Delhi NCR},
  author={Your Name},
  year={2025},
  url={https://github.com/YOUR_USERNAME/sentinel5p-delhi-air-quality}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/YOUR_USERNAME)

## 🙏 Acknowledgments

- AGH University - ML4SA2 Course
- Copernicus Programme for Sentinel-5P data
- Google Earth Engine for cloud processing
- ECMWF for ERA5 reanalysis data

## 📧 Contact

For questions or issues, please open an issue on GitHub or contact [your.email@example.com](mailto:your.email@example.com).

---

**Project Status:** ✅ Complete and ready for submission

**Last Updated:** January 2025
