# Quick Reference Guide

## First Time Setup

### 1. Create Conda Environment (Easiest)
```bash
setup_conda_env.bat
```
This will:
- Create a new conda environment
- Install all required packages
- Verify installation

### 2. Or Use Existing Environment
If environment already exists:
```bash
conda activate sentinel5p
```

## Daily Workflow

### Starting Work
```bash
# 1. Activate environment
conda activate sentinel5p

# 2. Navigate to project
cd D:\projSentinel

# 3. Start Jupyter (if using notebooks)
jupyter notebook
```

### Verify Setup
```bash
python scripts\setup_check.py
```

## Common Commands

### Environment Management
```bash
# Activate environment
conda activate sentinel5p

# Deactivate
conda deactivate

# List environments
conda env list

# Remove environment (if needed)
conda env remove -n sentinel5p
```

### Package Management
```bash
# Install new package
conda activate sentinel5p
pip install package_name

# Update requirements.txt after installing
pip freeze > requirements.txt
```

### Running Scripts
```bash
# Make sure environment is activated first!
conda activate sentinel5p

# Run Python script
python scripts\setup_check.py

# Run Jupyter notebook
jupyter notebook notebooks\00_setup_verification.ipynb
```

## Project Structure

```
projSentinel/
├── data/              # Data files (large, in .gitignore)
├── notebooks/         # Jupyter notebooks
├── scripts/           # Python scripts
├── outputs/           # Final outputs
├── config.py         # Project configuration
└── requirements.txt  # Python dependencies
```

## Next Steps After Setup

1. ✅ Environment created
2. ✅ Packages installed
3. Set up Google Earth Engine:
   ```bash
   conda activate sentinel5p
   python -c "import ee; ee.Authenticate()"
   ```
4. Start with: `notebooks/01_data_download.ipynb`

## Getting Help

- **Environment issues**: See `ENVIRONMENT_SETUP.md`
- **Installation issues**: See `INSTALL.md`
- **Project overview**: See `README.md`
- **Project plan**: See `PROJECT_PLAN.md`
