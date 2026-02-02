# Sentinel-5P Air Pollution Dynamics over Delhi NCR
## 5-Minute Presentation Outline

---

## Slide 1: Title Slide
**Sentinel-5P Air Pollution Dynamics over Delhi NCR**

*24-Month Analysis (Jan 2022 - Jan 2024)*

- NO₂, SO₂, CO, HCHO Analysis
- Local vs. Regional Transport Classification
- Source Attribution and Policy Implications

**AGH University - ML4SA2 Course Project**

---

## Slide 2: Problem Statement
**Why Delhi?**

- One of the world's most polluted cities
- Complex pollution sources: local + regional transport
- Need to distinguish:
  - **Local sources** (traffic, industry, power plants)
  - **Regional transport** (crop burning, upwind emissions)

**Research Question:**
*What fraction of Delhi's pollution is locally generated vs. transported from surrounding regions?*

---

## Slide 3: Methodology
**Data & Methods**

**Satellite Data:**
- Sentinel-5P TROPOMI (24 months)
- 4 pollutants: NO₂, SO₂, CO, HCHO
- Spatial resolution: ~1 km

**Meteorological Data:**
- ERA5 reanalysis wind data
- u-wind, v-wind components at 850 hPa

**Analysis:**
1. Monthly composites of pollution
2. Wind-based regime classification (local vs. advected)
3. Back-trajectory analysis for severe episodes
4. Hotspot identification

---

## Slide 4: Key Finding 1 - Pollution Regimes
**Local vs. Advected Pollution**

**Classification Results:**
- **62.5% of time:** Local pollution dominant (low wind conditions)
- **37.5% of time:** Regional transport dominant (high wind conditions)

**Implication:**
Delhi's pollution is a **mix of local and regional sources** - both need attention!

**Wind Speed Threshold:** 5.0 m/s
- < 5 m/s: Local accumulation
- ≥ 5 m/s: Regional transport

---

## Slide 5: Key Finding 2 - Seasonal Patterns
**Distinct Seasonal Behavior**

**Winter (Dec-Feb):**
- Elevated NO₂, SO₂
- Sources: Heating, power generation, calm conditions

**Post-Monsoon (Oct-Nov):**
- Peak CO, HCHO
- Sources: Crop residue burning in Punjab/Haryana

**Summer (Mar-May):**
- Moderate levels
- Regional transport patterns

**Monsoon (Jun-Sep):**
- Limited data (cloud cover)
- Natural cleansing effect

---

## Slide 6: Key Finding 3 - Source Attribution
**Where Does Pollution Come From?**

**Back-Trajectory Analysis (Severe Episodes):**

1. **Northwest (Punjab/Haryana):**
   - Crop burning regions
   - Peak in Oct-Nov
   - High CO, HCHO

2. **West (Industrial Belt):**
   - Power plants, industries
   - Year-round contribution
   - High SO₂, NO₂

3. **Local (Delhi NCR):**
   - Traffic, local industry
   - Dominant during calm conditions
   - All pollutants

---

## Slide 7: Multi-Pollutant Insights
**Pollutant-Specific Patterns**

**NO₂ (Nitrogen Dioxide):**
- Traffic and industrial emissions
- Higher during local regime
- Urban hotspots

**SO₂ (Sulfur Dioxide):**
- Power plants and industry
- Both local and regional sources
- Persistent hotspots

**CO (Carbon Monoxide):**
- Biomass burning (crop residue)
- Strong seasonal pattern
- Regional transport dominant

**HCHO (Formaldehyde):**
- Secondary pollution formation
- Biomass burning indicator
- Regional transport pattern

---

## Slide 8: Policy Implications
**What This Means for Air Quality Management**

**1. Local Action Required (62.5% of time)**
- Address Delhi's own emissions:
  - Traffic management
  - Industrial controls
  - Power plant regulations

**2. Regional Coordination Needed (37.5% of time)**
- Coordinate with neighboring states:
  - Crop burning management (Punjab/Haryana)
  - Industrial emission controls
  - Cross-state pollution transport

**3. Seasonal Strategies**
- Winter: Focus on local sources
- Post-monsoon: Address crop burning
- Year-round: Multi-pollutant approach

---

## Slide 9: Sentinel-5P Strengths & Limitations
**Satellite Data for Air Quality**

**Strengths:**
✓ Comprehensive spatial coverage
✓ Consistent temporal monitoring
✓ Multi-pollutant capability
✓ Regional transport analysis
✓ Free and open access

**Limitations:**
✗ Column vs. surface concentration mismatch
✗ Single daily overpass (misses diurnal variations)
✗ Cloud screening reduces data availability
✗ ~1 km resolution (not street-level)
✗ Requires validation with ground measurements

**Best Use:** Regional patterns, trends, transport analysis

---

## Slide 10: Conclusions
**Key Takeaways**

1. **Delhi's pollution is 62.5% local, 37.5% regional**
   - Both sources need attention

2. **Strong seasonal patterns**
   - Winter: Local sources
   - Post-monsoon: Regional crop burning

3. **Multi-pollutant approach essential**
   - Different pollutants show different patterns
   - Source-specific strategies needed

4. **Satellite data valuable for regional analysis**
   - Complements ground measurements
   - Enables transport pathway identification

**Recommendation:** Integrated local + regional air quality management strategy

---

## Slide 11: Thank You
**Questions?**

**Project Resources:**
- Complete analysis: `outputs/reports/Interpretive_Note_Sentinel5P_Delhi.md`
- Visualizations: `outputs/maps/`, `outputs/time_series/`
- Code: `scripts/`, `notebooks/01_complete_analysis.ipynb`

**Contact:**
Jakub Sumara - jsumara@student.agh.edu.pl
Zuzanna Słobodzian - zslobodzian@student.agh.edu.pl

**AGH University - ML4SA2 Course Project**

---

## Presentation Notes

### Timing (5 minutes):
- Slide 1: 15 seconds (Title)
- Slide 2: 30 seconds (Problem)
- Slide 3: 30 seconds (Methodology)
- Slide 4: 45 seconds (Key Finding 1)
- Slide 5: 45 seconds (Key Finding 2)
- Slide 6: 45 seconds (Key Finding 3)
- Slide 7: 30 seconds (Multi-pollutant)
- Slide 8: 45 seconds (Policy)
- Slide 9: 30 seconds (Strengths/Limitations)
- Slide 10: 30 seconds (Conclusions)
- Slide 11: 15 seconds (Thank you)

**Total: ~5 minutes**

### Visual Aids:
- Use maps from `outputs/maps/` (seasonal anomalies, source attribution)
- Use time series plots from `outputs/time_series/`
- Use animations from `outputs/animations/`
- Keep slides simple, one main point per slide

### Delivery Tips:
- Start with the problem (why Delhi matters)
- Emphasize the 62.5% / 37.5% split (key finding)
- Show visualizations for source attribution
- End with clear policy recommendations
- Be ready to discuss methodology if asked
