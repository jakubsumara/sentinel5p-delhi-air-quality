"""
Main Analysis Workflow
======================

This script runs the complete analysis pipeline for Sentinel-5P air pollution
analysis over Delhi NCR.

Usage:
    python run_analysis.py [--step STEP] [--pollutant POLLUTANT]

Steps:
    1. setup       - Verify environment and dependencies
    2. download    - Download data (Sentinel-5P and ERA5)
    3. process     - Process raw data into composites
    4. analyze     - Run trajectory and hotspot analysis
    5. visualize   - Generate all visualizations
    6. all         - Run all steps (default)

Example:
    python run_analysis.py --step all
    python run_analysis.py --step process --pollutant NO2
"""

import os
import sys
import argparse
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

def run_setup():
    """Step 1: Verify environment setup."""
    print("="*70)
    print("STEP 1: Environment Setup Verification")
    print("="*70)
    
    from setup_check import main as check_setup
    check_setup()
    
    print("\n" + "="*70)
    print("Setup verification complete!")
    print("="*70)
    print("\nNext steps:")
    print("  1. If packages are missing, run: pip install -r requirements.txt")
    print("  2. Set up Google Earth Engine: python scripts/setup_gee.py")
    print("  3. Set up ERA5 access: See ERA5_SETUP.md")
    print("="*70 + "\n")

def run_download(pollutant=None):
    """Step 2: Download data."""
    print("="*70)
    print("STEP 2: Data Download")
    print("="*70)
    
    print("\nNote: Data download requires:")
    print("  - Google Earth Engine authentication (for Sentinel-5P)")
    print("  - Copernicus CDS API setup (for ERA5)")
    print("\nSee GEE_SETUP.md and ERA5_SETUP.md for instructions.")
    
    choice = input("\nProceed with download? (y/n): ").strip().lower()
    if choice != 'y':
        print("Skipping download step.")
        return
    
    # Download Sentinel-5P data
    print("\n" + "-"*70)
    print("Downloading Sentinel-5P data from Google Earth Engine...")
    print("-"*70)
    try:
        from download_gee import main as download_gee
        download_gee()
    except Exception as e:
        print(f"[WARNING] GEE download failed: {e}")
        print("You may need to download files manually from Google Drive.")
    
    # Download ERA5 data
    print("\n" + "-"*70)
    print("Downloading ERA5 wind data from Copernicus CDS...")
    print("-"*70)
    try:
        from download_era5 import main as download_era5
        download_era5()
    except Exception as e:
        print(f"[WARNING] ERA5 download failed: {e}")
        print("See ERA5_SETUP.md for manual setup instructions.")
    
    print("\n" + "="*70)
    print("Download step complete!")
    print("="*70)
    print("\nNote: If using Google Earth Engine, files will be exported to")
    print("Google Drive. Download them manually and place in data/processed/")
    print("="*70 + "\n")

def run_process(pollutant=None):
    """Step 3: Process raw data."""
    print("="*70)
    print("STEP 3: Data Processing")
    print("="*70)
    
    # Process ERA5 data
    print("\n" + "-"*70)
    print("Processing ERA5 wind data...")
    print("-"*70)
    try:
        from process_era5 import main as process_era5
        import argparse as ap
        args = ap.Namespace(input='data/era5', output=None)
        process_era5(args)
    except Exception as e:
        print(f"[WARNING] ERA5 processing failed: {e}")
    
    # Process Sentinel-5P data
    print("\n" + "-"*70)
    print("Processing Sentinel-5P data...")
    print("-"*70)
    try:
        from process_sentinel5p import main as process_s5p
        import argparse as ap
        args = ap.Namespace(
            input='data/processed',
            pollutant=pollutant,
            output='data/processed'
        )
        process_s5p(args)
    except Exception as e:
        print(f"[WARNING] Sentinel-5P processing failed: {e}")
        print("Make sure GeoTIFF files are in data/processed/")
    
    print("\n" + "="*70)
    print("Processing step complete!")
    print("="*70 + "\n")

def run_analyze(pollutant=None):
    """Step 4: Run analysis."""
    print("="*70)
    print("STEP 4: Analysis")
    print("="*70)
    
    # Trajectory analysis
    print("\n" + "-"*70)
    print("Running trajectory analysis...")
    print("-"*70)
    try:
        from trajectory_analysis import main as trajectory_analysis
        trajectory_analysis()
    except Exception as e:
        print(f"[ERROR] Trajectory analysis failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Hotspot analysis
    print("\n" + "-"*70)
    print("Running hotspot analysis...")
    print("-"*70)
    try:
        from hotspot_analysis import main as hotspot_analysis
        hotspot_analysis()
    except Exception as e:
        print(f"[ERROR] Hotspot analysis failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("Analysis step complete!")
    print("="*70 + "\n")

def run_visualize(pollutant=None):
    """Step 5: Generate visualizations."""
    print("="*70)
    print("STEP 5: Visualization")
    print("="*70)
    
    # Time series plots
    print("\n" + "-"*70)
    print("Creating time series plots...")
    print("-"*70)
    try:
        from visualize import main as visualize
        visualize()
    except Exception as e:
        print(f"[ERROR] Visualization failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Map visualizations
    print("\n" + "-"*70)
    print("Creating map visualizations...")
    print("-"*70)
    try:
        from create_maps import main as create_maps
        create_maps()
    except Exception as e:
        print(f"[ERROR] Map creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Source attribution maps
    print("\n" + "-"*70)
    print("Creating source attribution maps...")
    print("-"*70)
    try:
        from create_source_attribution import main as create_source
        create_source()
    except Exception as e:
        print(f"[ERROR] Source attribution failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("Visualization step complete!")
    print("="*70)
    print("\nOutputs saved in:")
    print("  - outputs/time_series/")
    print("  - outputs/maps/")
    print("  - outputs/animations/")
    print("="*70 + "\n")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Run Sentinel-5P air pollution analysis pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--step',
        choices=['setup', 'download', 'process', 'analyze', 'visualize', 'all'],
        default='all',
        help='Which step to run (default: all)'
    )
    
    parser.add_argument(
        '--pollutant',
        choices=['NO2', 'SO2', 'CO', 'HCHO'],
        default=None,
        help='Process specific pollutant only (optional)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("Sentinel-5P Air Pollution Analysis - Delhi NCR")
    print("="*70)
    print(f"Step: {args.step}")
    if args.pollutant:
        print(f"Pollutant: {args.pollutant}")
    print("="*70 + "\n")
    
    if args.step == 'setup' or args.step == 'all':
        run_setup()
        if args.step == 'setup':
            return
    
    if args.step == 'download' or args.step == 'all':
        run_download(args.pollutant)
        if args.step == 'download':
            return
    
    if args.step == 'process' or args.step == 'all':
        run_process(args.pollutant)
        if args.step == 'process':
            return
    
    if args.step == 'analyze' or args.step == 'all':
        run_analyze(args.pollutant)
        if args.step == 'analyze':
            return
    
    if args.step == 'visualize' or args.step == 'all':
        run_visualize(args.pollutant)
        if args.step == 'visualize':
            return
    
    print("\n" + "="*70)
    print("Analysis pipeline complete!")
    print("="*70)
    print("\nAll outputs are in the outputs/ directory.")
    print("See outputs/reports/ for the interpretive note.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
