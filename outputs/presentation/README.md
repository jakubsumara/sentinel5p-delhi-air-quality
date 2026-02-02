# 5-Minute Presentation

## Overview

This presentation covers the key findings from the Sentinel-5P air pollution analysis over Delhi NCR (24 months, Jan 2022 - Jan 2024).

## Files

### Presentation Slides (PNG Images)
- `slide_01_title.png` - Title slide
- `slide_02_problem.png` - Problem statement
- `slide_03_methodology.png` - Data and methods
- `slide_04_key_finding_1.png` - Pollution regimes (local vs. advected)
- `slide_05_key_finding_2.png` - Seasonal patterns
- `slide_10_conclusions.png` - Conclusions and recommendations
- `slide_11_thank_you.png` - Thank you slide

### Presentation Outline
- `Presentation_Outline.md` - Complete slide-by-slide outline with notes

## Usage

### Option 1: Use Generated PNG Slides
1. Import slides into PowerPoint, Google Slides, or presentation software
2. Add additional slides from the outline as needed
3. Include visualizations from `outputs/maps/` and `outputs/time_series/`

### Option 2: Create from Outline
1. Use `Presentation_Outline.md` as a guide
2. Create slides in your preferred presentation software
3. Include visualizations from the analysis outputs

### Option 3: Generate More Slides
Run the script to generate additional slides:
```bash
python scripts/create_presentation.py
```

## Key Messages (5 Minutes)

### 1. Problem (30 seconds)
- Delhi is one of the world's most polluted cities
- Need to distinguish local vs. regional sources

### 2. Methodology (30 seconds)
- Sentinel-5P satellite data (24 months)
- ERA5 wind data for transport analysis
- 4 pollutants: NO₂, SO₂, CO, HCHO

### 3. Key Finding 1 (45 seconds)
- **62.5% local, 37.5% regional**
- Both sources need attention
- Wind speed threshold: 5.0 m/s

### 4. Key Finding 2 (45 seconds)
- Strong seasonal patterns:
  - Winter: Local sources (NO₂, SO₂)
  - Post-monsoon: Regional crop burning (CO, HCHO)

### 5. Source Attribution (45 seconds)
- Back-trajectory analysis shows:
  - Northwest: Crop burning (Punjab/Haryana)
  - West: Industrial sources
  - Local: Delhi's own emissions

### 6. Policy Implications (45 seconds)
- Local action required (62.5% of time)
- Regional coordination needed (37.5% of time)
- Seasonal strategies

### 7. Conclusions (30 seconds)
- Integrated local + regional management strategy
- Multi-pollutant approach essential
- Satellite data valuable for regional analysis

## Visual Aids

Include these visualizations in your presentation:

1. **Seasonal Anomaly Maps** (`outputs/maps/*_seasonal_anomaly.png`)
   - Show seasonal patterns visually

2. **Source Attribution Maps** (`outputs/maps/*_source_attribution.png`)
   - Show back-trajectories for severe episodes

3. **Time Series Plots** (`outputs/time_series/*_regime_comparison.png`)
   - Show local vs. advected comparison

4. **Animations** (`outputs/animations/*_animation.gif`)
   - Show temporal evolution (optional, if time permits)

## Timing Guide

- **Slide 1 (Title):** 15 seconds
- **Slide 2 (Problem):** 30 seconds
- **Slide 3 (Methodology):** 30 seconds
- **Slide 4 (Key Finding 1):** 45 seconds
- **Slide 5 (Key Finding 2):** 45 seconds
- **Additional slides:** 2-3 minutes
- **Slide 10 (Conclusions):** 30 seconds
- **Slide 11 (Thank you):** 15 seconds

**Total: ~5 minutes**

## Tips for Delivery

1. **Start strong:** Emphasize why Delhi matters
2. **Highlight key number:** 62.5% / 37.5% split is the main finding
3. **Use visuals:** Maps and plots are more impactful than text
4. **Be concise:** One main point per slide
5. **End clearly:** Policy recommendations should be actionable

## Additional Resources

- **Complete Analysis:** `outputs/reports/Interpretive_Note_Sentinel5P_Delhi.md`
- **All Visualizations:** `outputs/maps/`, `outputs/time_series/`
- **Code:** `scripts/`, `notebooks/01_complete_analysis.ipynb`

## Next Steps

1. Review generated slides
2. Add visualizations from analysis outputs
3. Practice timing (5 minutes)
4. Prepare for questions on:
   - Methodology (wind classification, trajectory analysis)
   - Limitations of satellite data
   - Policy recommendations
