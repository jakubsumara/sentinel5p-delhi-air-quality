"""
Verification Script for Project Completion
Checks all requirements from AGH-ML4SA2-term-paper.pdf
"""

import os
import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_file_exists(filepath, description):
    """Check if file exists and report status."""
    exists = os.path.exists(filepath)
    status = "[OK]" if exists else "[MISSING]"
    print(f"{status} {description}: {filepath}")
    return exists

def main():
    """Main verification function."""
    print("="*70)
    print("PROJECT COMPLETION VERIFICATION")
    print("Based on: AGH-ML4SA2-term-paper.pdf")
    print("="*70)
    
    all_good = True
    
    # Expected Outcomes
    print("\n" + "="*70)
    print("1. EXPECTED OUTCOMES")
    print("="*70)
    
    # 1.1 Gridded 24-month maps and animations
    print("\n1.1 Gridded 24-Month Maps and Animations:")
    pollutants = ['NO2', 'SO2', 'CO', 'HCHO']
    
    # Seasonal anomaly maps
    for p in pollutants:
        filepath = f"outputs/maps/{p}_seasonal_anomaly.png"
        if not check_file_exists(filepath, f"{p} seasonal anomaly"):
            all_good = False
    
    # Sample monthly maps
    sample_months = ['202201', '202301', '202312']
    for p in pollutants:
        for month in sample_months:
            filepath = f"outputs/maps/{p}_{month}_map.png"
            if not check_file_exists(filepath, f"{p} {month} map"):
                all_good = False
    
    # Animations
    for p in pollutants:
        filepath = f"outputs/animations/{p}_animation.gif"
        if not check_file_exists(filepath, f"{p} animation"):
            all_good = False
    
    # 1.2 Time-series plots with regime decomposition
    print("\n1.2 Time-Series Plots with Regime Decomposition:")
    for p in pollutants:
        ts_file = f"outputs/time_series/{p}_timeseries.png"
        reg_file = f"outputs/time_series/{p}_regime_comparison.png"
        if not check_file_exists(ts_file, f"{p} time series"):
            all_good = False
        if not check_file_exists(reg_file, f"{p} regime comparison"):
            all_good = False
    
    # 1.3 Source-region attribution maps
    print("\n1.3 Source-Region Attribution Maps:")
    for p in pollutants:
        filepath = f"outputs/maps/{p}_source_attribution.png"
        if not check_file_exists(filepath, f"{p} source attribution"):
            all_good = False
    
    # 1.4 Interpretive note
    print("\n1.4 Interpretive Note:")
    note_file = "outputs/reports/Interpretive_Note_Sentinel5P_Delhi.md"
    if not check_file_exists(note_file, "Interpretive note"):
        all_good = False
    else:
        # Check content
        with open(note_file, 'r', encoding='utf-8') as f:
            content = f.read()
            required_topics = [
                'column vs. surface',
                'cloud screening',
                'overpass time',
                'strengths',
                'limitations'
            ]
            for topic in required_topics:
                if topic.lower() in content.lower():
                    print(f"  [OK] Contains discussion of: {topic}")
                else:
                    print(f"  [MISSING] Missing discussion of: {topic}")
                    all_good = False
    
    # Processed Data Files
    print("\n" + "="*70)
    print("2. PROCESSED DATA FILES")
    print("="*70)
    
    for p in pollutants:
        print(f"\n{p}:")
        ts_file = f"data/processed/{p}_timeseries.csv"
        cls_file = f"data/processed/{p}_classified.csv"
        comp_file = f"data/processed/{p}_monthly_composite.nc"
        sev_file = f"data/processed/{p}_severe_episodes.csv"
        hot_file = f"data/processed/{p}_hotspots.csv"
        
        check_file_exists(ts_file, "  Time series CSV")
        check_file_exists(cls_file, "  Classified data CSV")
        check_file_exists(comp_file, "  Monthly composite NetCDF")
        check_file_exists(sev_file, "  Severe episodes CSV")
        check_file_exists(hot_file, "  Hotspots CSV")
    
    # Code Organization
    print("\n" + "="*70)
    print("3. CODE ORGANIZATION & REPRODUCIBILITY")
    print("="*70)
    
    code_files = [
        ("run_analysis.py", "Main workflow script"),
        ("notebooks/01_complete_analysis.ipynb", "Interactive notebook"),
        ("WORKFLOW.md", "Workflow documentation"),
        ("CODE_ORGANIZATION.md", "Code organization docs"),
        ("README.md", "Project README"),
        ("requirements.txt", "Dependencies list"),
        ("config.py", "Configuration file")
    ]
    
    for filepath, description in code_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Presentation
    print("\n" + "="*70)
    print("4. PRESENTATION (5 MINUTES)")
    print("="*70)
    
    pres_files = [
        "outputs/presentation/slide_01_title.png",
        "outputs/presentation/slide_02_problem.png",
        "outputs/presentation/slide_03_methodology.png",
        "outputs/presentation/slide_04_key_finding_1.png",
        "outputs/presentation/slide_05_key_finding_2.png",
        "outputs/presentation/slide_10_conclusions.png",
        "outputs/presentation/slide_11_thank_you.png",
        "outputs/presentation/Presentation_Outline.md",
        "outputs/presentation/README.md"
    ]
    
    for filepath in pres_files:
        desc = os.path.basename(filepath)
        if not check_file_exists(filepath, desc):
            all_good = False
    
    # Final Summary
    print("\n" + "="*70)
    if all_good:
        print("[SUCCESS] ALL REQUIREMENTS COMPLETE!")
        print("="*70)
        print("\nProject is ready for submission!")
        print("\nNext steps:")
        print("  1. Review all outputs in outputs/ directory")
        print("  2. Practice presentation (5 minutes)")
        print("  3. Submit by 31st January")
        print("  4. Prepare for presentations in first week of February")
    else:
        print("[WARNING] SOME REQUIREMENTS MISSING")
        print("="*70)
        print("\nPlease check the missing files above.")
    
    print("="*70)

if __name__ == "__main__":
    main()
