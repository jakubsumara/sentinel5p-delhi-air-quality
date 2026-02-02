# Environment Setup Guide

This guide explains how to set up a dedicated conda environment for the Sentinel-5P project.

## Why Use a Separate Environment?

- **Isolation**: Keeps project dependencies separate from your base Python installation
- **Reproducibility**: Ensures consistent package versions across different machines
- **Clean**: Easy to delete and recreate if something goes wrong
- **Best Practice**: Standard practice in Python data science projects

## Quick Setup (Automated)

### Windows:
```bash
setup_conda_env.bat
```

### Linux/Mac:
```bash
chmod +x setup_conda_env.sh
./setup_conda_env.sh
```

## Manual Setup

### Step 1: Create Conda Environment

```bash
conda create -n sentinel5p python=3.11
```

This creates a new environment named `sentinel5p` with Python 3.11.

### Step 2: Activate the Environment

```bash
conda activate sentinel5p
```

You should see `(sentinel5p)` in your prompt instead of `(base)`.

### Step 3: Navigate to Project

```bash
cd D:\projSentinel
```

### Step 4: Install Packages

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
python scripts\setup_check.py
```

## Using the Environment

### Activating (Every Time You Work on the Project)

```bash
conda activate sentinel5p
cd D:\projSentinel
```

### Deactivating

```bash
conda deactivate
```

### Checking Active Environment

```bash
conda info --envs
```

The active environment will have an asterisk (*) next to it.

## Jupyter Notebook Setup

If you want to use this environment in Jupyter:

```bash
conda activate sentinel5p
conda install ipykernel -y
python -m ipykernel install --user --name sentinel5p --display-name "Python (sentinel5p)"
```

Then in Jupyter, you can select "Python (sentinel5p)" as your kernel.

## Managing the Environment

### List All Environments
```bash
conda env list
```

### Remove Environment (if needed)
```bash
conda env remove -n sentinel5p
```

### Export Environment (for sharing)
```bash
conda activate sentinel5p
conda env export > environment.yml
```

### Recreate from Export
```bash
conda env create -f environment.yml
```

## Troubleshooting

### "Conda command not found"
- Make sure Anaconda/Miniconda is installed
- On Windows, restart your terminal after installation
- On Linux/Mac, add conda to PATH: `export PATH="$HOME/anaconda3/bin:$PATH"`

### "Environment already exists"
If the environment already exists, you can:
- Remove it: `conda env remove -n sentinel5p`
- Or use it: `conda activate sentinel5p`

### Packages Not Installing
- Make sure environment is activated: `conda activate sentinel5p`
- Try: `conda install pip` first, then use pip

### Jupyter Can't See Environment
- Install ipykernel: `conda install ipykernel`
- Register kernel: `python -m ipykernel install --user --name sentinel5p`

## Alternative: Using venv (Standard Python)

If you prefer not to use conda:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
python -m pip install -r requirements.txt
```

## Next Steps

After setting up the environment:

1. ✅ Environment created and activated
2. Install packages (if not done automatically)
3. Set up Google Earth Engine: `python -c "import ee; ee.Authenticate()"`
4. Start working on the project!
