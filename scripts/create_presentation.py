"""
Create 5-Minute Presentation Slides
Generates visual slides for the presentation using matplotlib.
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 14
plt.rcParams['figure.figsize'] = (16, 9)  # 16:9 aspect ratio for presentations

def create_title_slide(output_dir='outputs/presentation'):
    """Create title slide."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off')
    
    # Title
    title = ax.text(0.5, 0.7, 'Sentinel-5P Air Pollution Dynamics\nover Delhi NCR',
                   ha='center', va='center', fontsize=48, fontweight='bold',
                   transform=ax.transAxes)
    
    # Subtitle
    subtitle = ax.text(0.5, 0.5, '24-Month Analysis (Jan 2022 - Jan 2024)',
                      ha='center', va='center', fontsize=28,
                      transform=ax.transAxes, style='italic')
    
    # Bullet points
    bullets = [
        'NO₂, SO₂, CO, HCHO Analysis',
        'Local vs. Regional Transport Classification',
        'Source Attribution and Policy Implications'
    ]
    
    y_start = 0.35
    for i, bullet in enumerate(bullets):
        ax.text(0.5, y_start - i*0.08, f'• {bullet}',
               ha='center', va='center', fontsize=20,
               transform=ax.transAxes)
    
    # Footer
    ax.text(0.5, 0.05, 'AGH University - ML4SA2 Course Project',
           ha='center', va='center', fontsize=18,
           transform=ax.transAxes, style='italic')
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'slide_01_title.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Created: {output_file}")

def create_problem_slide(output_dir='outputs/presentation'):
    """Create problem statement slide."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.9, 'Why Delhi?', ha='center', va='top',
           fontsize=42, fontweight='bold', transform=ax.transAxes)
    
    # Problem points
    problems = [
        'One of the world\'s most polluted cities',
        'Complex pollution sources: local + regional transport',
        'Need to distinguish:',
        '  • Local sources (traffic, industry, power plants)',
        '  • Regional transport (crop burning, upwind emissions)'
    ]
    
    y_start = 0.7
    for i, problem in enumerate(problems):
        fontsize = 24 if i == 0 else 20
        ax.text(0.1, y_start - i*0.12, problem,
               ha='left', va='top', fontsize=fontsize,
               transform=ax.transAxes)
    
    # Research question box
    box = FancyBboxPatch((0.1, 0.25), 0.8, 0.15,
                         boxstyle="round,pad=0.02", 
                         edgecolor='darkblue', facecolor='lightblue',
                         linewidth=3, transform=ax.transAxes)
    ax.add_patch(box)
    
    ax.text(0.5, 0.33, 'Research Question:', ha='center', va='center',
           fontsize=22, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.28, 'What fraction of Delhi\'s pollution is locally\ngenerated vs. transported from surrounding regions?',
           ha='center', va='center', fontsize=20, style='italic',
           transform=ax.transAxes)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'slide_02_problem.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Created: {output_file}")

def create_methodology_slide(output_dir='outputs/presentation'):
    """Create methodology slide."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.9, 'Data & Methods', ha='center', va='top',
           fontsize=42, fontweight='bold', transform=ax.transAxes)
    
    # Satellite Data
    ax.text(0.1, 0.75, 'Satellite Data:', ha='left', va='top',
           fontsize=24, fontweight='bold', transform=ax.transAxes)
    sat_points = [
        '• Sentinel-5P TROPOMI (24 months)',
        '• 4 pollutants: NO₂, SO₂, CO, HCHO',
        '• Spatial resolution: ~1 km'
    ]
    for i, point in enumerate(sat_points):
        ax.text(0.15, 0.68 - i*0.08, point, ha='left', va='top',
               fontsize=18, transform=ax.transAxes)
    
    # Meteorological Data
    ax.text(0.1, 0.45, 'Meteorological Data:', ha='left', va='top',
           fontsize=24, fontweight='bold', transform=ax.transAxes)
    met_points = [
        '• ERA5 reanalysis wind data',
        '• u-wind, v-wind components at 850 hPa'
    ]
    for i, point in enumerate(met_points):
        ax.text(0.15, 0.38 - i*0.08, point, ha='left', va='top',
               fontsize=18, transform=ax.transAxes)
    
    # Analysis
    ax.text(0.1, 0.25, 'Analysis:', ha='left', va='top',
           fontsize=24, fontweight='bold', transform=ax.transAxes)
    analysis_points = [
        '1. Monthly composites of pollution',
        '2. Wind-based regime classification (local vs. advected)',
        '3. Back-trajectory analysis for severe episodes',
        '4. Hotspot identification'
    ]
    for i, point in enumerate(analysis_points):
        ax.text(0.15, 0.18 - i*0.07, point, ha='left', va='top',
               fontsize=18, transform=ax.transAxes)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'slide_03_methodology.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Created: {output_file}")

def create_key_finding_1_slide(output_dir='outputs/presentation'):
    """Create key finding 1 slide - pollution regimes."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.9, 'Key Finding 1: Pollution Regimes', ha='center', va='top',
           fontsize=42, fontweight='bold', transform=ax.transAxes)
    
    # Classification Results
    ax.text(0.5, 0.75, 'Local vs. Advected Pollution', ha='center', va='top',
           fontsize=28, fontweight='bold', transform=ax.transAxes)
    
    # Create pie chart or bar chart
    categories = ['Local', 'Advected']
    percentages = [62.5, 37.5]
    colors = ['#ff6b6b', '#4ecdc4']
    
    # Bar chart
    bars = ax.barh([0.5, 0.35], percentages, height=0.08, color=colors,
                   transform=ax.transAxes)
    
    # Add percentage labels
    for i, (cat, pct) in enumerate(zip(categories, percentages)):
        ax.text(pct/2, 0.5 - i*0.15, f'{cat}\n{pct}%',
               ha='center', va='center', fontsize=32, fontweight='bold',
               color='white', transform=ax.transAxes)
        ax.text(pct + 2, 0.5 - i*0.15, f'{pct}% of time',
               ha='left', va='center', fontsize=24,
               transform=ax.transAxes)
    
    # Implication
    box = FancyBboxPatch((0.1, 0.15), 0.8, 0.1,
                         boxstyle="round,pad=0.02",
                         edgecolor='darkgreen', facecolor='lightgreen',
                         linewidth=3, transform=ax.transAxes)
    ax.add_patch(box)
    
    ax.text(0.5, 0.2, 'Implication:', ha='center', va='center',
           fontsize=22, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.16, 'Delhi\'s pollution is a mix of local and regional sources - both need attention!',
           ha='center', va='center', fontsize=20, style='italic',
           transform=ax.transAxes)
    
    # Wind threshold
    ax.text(0.5, 0.05, 'Wind Speed Threshold: 5.0 m/s',
           ha='center', va='center', fontsize=18,
           transform=ax.transAxes, style='italic')
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'slide_04_key_finding_1.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Created: {output_file}")

def create_key_finding_2_slide(output_dir='outputs/presentation'):
    """Create key finding 2 slide - seasonal patterns."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.9, 'Key Finding 2: Seasonal Patterns', ha='center', va='top',
           fontsize=42, fontweight='bold', transform=ax.transAxes)
    
    seasons = [
        ('Winter (Dec-Feb)', 'Elevated NO₂, SO₂', 'Heating, power generation, calm conditions', '#3498db'),
        ('Post-Monsoon (Oct-Nov)', 'Peak CO, HCHO', 'Crop residue burning in Punjab/Haryana', '#e74c3c'),
        ('Summer (Mar-May)', 'Moderate levels', 'Regional transport patterns', '#f39c12'),
        ('Monsoon (Jun-Sep)', 'Limited data', 'Natural cleansing effect', '#2ecc71')
    ]
    
    y_start = 0.75
    for i, (season, pattern, source, color) in enumerate(seasons):
        y_pos = y_start - i*0.16
        
        # Season box
        box = FancyBboxPatch((0.1, y_pos - 0.06), 0.8, 0.12,
                           boxstyle="round,pad=0.01",
                           edgecolor=color, facecolor=color, alpha=0.2,
                           linewidth=2, transform=ax.transAxes)
        ax.add_patch(box)
        
        ax.text(0.15, y_pos, season, ha='left', va='center',
               fontsize=22, fontweight='bold', transform=ax.transAxes)
        ax.text(0.15, y_pos - 0.03, f'{pattern} • {source}',
               ha='left', va='center', fontsize=18,
               transform=ax.transAxes)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'slide_05_key_finding_2.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Created: {output_file}")

def create_conclusions_slide(output_dir='outputs/presentation'):
    """Create conclusions slide."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.9, 'Conclusions', ha='center', va='top',
           fontsize=42, fontweight='bold', transform=ax.transAxes)
    
    conclusions = [
        ('1. Delhi\'s pollution is 62.5% local, 37.5% regional',
         'Both sources need attention'),
        ('2. Strong seasonal patterns',
         'Winter: Local sources | Post-monsoon: Regional crop burning'),
        ('3. Multi-pollutant approach essential',
         'Different pollutants show different patterns'),
        ('4. Satellite data valuable for regional analysis',
         'Complements ground measurements, enables transport pathway identification')
    ]
    
    y_start = 0.75
    for i, (main, detail) in enumerate(conclusions):
        y_pos = y_start - i*0.15
        
        ax.text(0.1, y_pos, main, ha='left', va='center',
               fontsize=22, fontweight='bold', transform=ax.transAxes)
        ax.text(0.15, y_pos - 0.04, detail, ha='left', va='center',
               fontsize=18, style='italic', transform=ax.transAxes)
    
    # Recommendation box
    box = FancyBboxPatch((0.1, 0.1), 0.8, 0.08,
                         boxstyle="round,pad=0.02",
                         edgecolor='darkred', facecolor='lightcoral',
                         linewidth=3, transform=ax.transAxes)
    ax.add_patch(box)
    
    ax.text(0.5, 0.14, 'Recommendation:', ha='center', va='center',
           fontsize=24, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.11, 'Integrated local + regional air quality management strategy',
           ha='center', va='center', fontsize=20, style='italic',
           transform=ax.transAxes)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'slide_10_conclusions.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Created: {output_file}")

def create_thank_you_slide(output_dir='outputs/presentation'):
    """Create thank you slide."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.6, 'Thank You!', ha='center', va='center',
           fontsize=56, fontweight='bold', transform=ax.transAxes)
    
    ax.text(0.5, 0.45, 'Questions?', ha='center', va='center',
           fontsize=36, transform=ax.transAxes)
    
    # Resources
    ax.text(0.5, 0.3, 'Project Resources:', ha='center', va='center',
           fontsize=24, fontweight='bold', transform=ax.transAxes)
    
    resources = [
        'Complete analysis: outputs/reports/',
        'Visualizations: outputs/maps/, outputs/time_series/',
        'Code: scripts/, notebooks/01_complete_analysis.ipynb'
    ]
    
    for i, resource in enumerate(resources):
        ax.text(0.5, 0.22 - i*0.06, resource, ha='center', va='center',
               fontsize=18, transform=ax.transAxes)
    
    # Footer
    ax.text(0.5, 0.05, 'AGH University - ML4SA2 Course Project',
           ha='center', va='center', fontsize=20, style='italic',
           transform=ax.transAxes)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'slide_11_thank_you.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Created: {output_file}")

def main():
    """Create all presentation slides."""
    print("="*70)
    print("Creating 5-Minute Presentation Slides")
    print("="*70)
    
    create_title_slide()
    create_problem_slide()
    create_methodology_slide()
    create_key_finding_1_slide()
    create_key_finding_2_slide()
    create_conclusions_slide()
    create_thank_you_slide()
    
    print("\n" + "="*70)
    print("[OK] Presentation slides created!")
    print("="*70)
    print("\nSlides saved in: outputs/presentation/")
    print("\nNote: Additional slides (source attribution, multi-pollutant,")
    print("policy implications, strengths/limitations) can be created")
    print("using the outline in: outputs/presentation/Presentation_Outline.md")
    print("="*70)

if __name__ == "__main__":
    main()
