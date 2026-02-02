# Interpretive Note: Sentinel-5P Strengths and Limitations for Delhi Air Quality Studies

## Executive Summary

This note evaluates the use of Sentinel-5P TROPOMI satellite data for air quality monitoring over Delhi NCR, based on 24 months of analysis (January 2022 - January 2024) of four key pollutants: NO₂, SO₂, CO, and HCHO. The analysis reveals both the significant potential and important limitations of satellite-based monitoring for urban air quality management.

---

## 1. Strengths of Sentinel-5P for Delhi Air Quality Studies

### 1.1 Comprehensive Spatial Coverage

**Advantage:** Sentinel-5P provides daily global coverage with a spatial resolution of ~3.5 × 7 km² (Level-2) or ~1 km² (Level-3 gridded products), offering complete spatial coverage of Delhi NCR and surrounding regions.

**Application:** This enables:
- Identification of pollution hotspots across the entire metropolitan area
- Mapping of pollution gradients from urban center to suburbs
- Detection of regional pollution sources (e.g., crop burning in Punjab/Haryana)
- Monitoring of pollution transport pathways

**Example from this study:** Our analysis successfully identified persistent pollution patterns across Delhi NCR and traced transport from upwind agricultural regions during post-monsoon months.

### 1.2 Consistent Temporal Monitoring

**Advantage:** Daily overpasses provide consistent, long-term monitoring without gaps due to instrument failures or maintenance (unlike ground-based stations).

**Application:**
- 24-month continuous time series without missing data
- Detection of pollution trends and seasonal patterns
- Identification of extreme events (e.g., Diwali, crop burning seasons)
- Long-term trend analysis for policy evaluation

**Example from this study:** We identified clear seasonal patterns:
- **Winter (Dec-Feb):** Elevated NO₂ and SO₂ from heating and power generation
- **Post-monsoon (Oct-Nov):** Peak CO and HCHO from crop residue burning
- **Summer (Mar-May):** Moderate levels with regional transport

### 1.3 Multi-Pollutant Capability

**Advantage:** Single instrument measures multiple pollutants simultaneously, providing source attribution:
- **NO₂:** Traffic and industrial emissions
- **SO₂:** Power plants and industrial sources
- **CO:** Biomass burning and incomplete combustion
- **HCHO:** Secondary pollution formation

**Application:** Multi-pollutant analysis enables:
- Source identification (e.g., distinguishing traffic vs. industrial vs. biomass burning)
- Pollution chemistry studies (e.g., secondary formation via HCHO)
- Comprehensive air quality assessment

**Example from this study:** Combined analysis revealed that Delhi's pollution is a mix of:
- **Local sources (62.5% of time):** Traffic, industry, power plants
- **Regional transport (37.5% of time):** Crop burning, upwind industrial areas

### 1.4 Regional Context and Transport Analysis

**Advantage:** Satellite data covers large areas, enabling analysis of regional pollution transport.

**Application:**
- Back-trajectory analysis to identify source regions
- Mapping of pollution plumes from surrounding states
- Quantification of local vs. transported pollution

**Example from this study:** Trajectory analysis showed that severe pollution episodes often originate from:
- **Northwest:** Punjab/Haryana crop burning regions (Oct-Nov)
- **West:** Industrial areas and power plants
- **Local:** Delhi's own emissions during calm conditions

### 1.5 Free and Open Access

**Advantage:** Sentinel-5P data is freely available through Copernicus Data Space Ecosystem and Google Earth Engine, making it accessible for research and policy support.

**Application:**
- No cost barriers for researchers and policymakers
- Easy integration with other datasets (e.g., ERA5 meteorological data)
- Reproducible analysis workflows

---

## 2. Limitations and Challenges

### 2.1 Column vs. Surface Concentration Mismatch

**Critical Limitation:** Sentinel-5P measures **total column** concentrations (molecules per m² from surface to top of atmosphere), not **surface** concentrations (what people breathe).

**Impact:**
- Column measurements include pollution throughout the entire atmospheric column
- Surface concentrations (relevant for health) can differ significantly
- Vertical mixing and boundary layer height affect the relationship

**Example:** A high NO₂ column might indicate:
- High surface pollution (worst case for health)
- Pollution aloft with clean surface air (less concerning)
- Mixed conditions (moderate concern)

**Mitigation:** 
- Combine with ground-based measurements for validation
- Use boundary layer height data to estimate surface concentrations
- Focus on relative changes rather than absolute values

### 2.2 Temporal Resolution Limitations

**Limitation:** Single daily overpass (~13:30 local time) provides only one snapshot per day.

**Impact:**
- Misses diurnal variations (morning rush hour, evening peaks)
- May miss short-duration pollution events
- Cannot capture rapid changes during the day

**Example:** Delhi's traffic-related NO₂ peaks in morning (8-10 AM) and evening (6-8 PM), but Sentinel-5P only captures midday conditions.

**Mitigation:**
- Combine with ground-based continuous monitors
- Use monthly/weekly composites to smooth temporal gaps
- Focus on seasonal and long-term trends rather than daily variations

### 2.3 Cloud Screening and Data Availability

**Limitation:** Cloud cover reduces data availability, especially during monsoon season (June-September).

**Impact:**
- **Monsoon months:** Limited data due to cloud cover
- **Winter months:** Better data availability
- **Data gaps:** Can miss important pollution events

**Example from this study:** Data availability was lowest during monsoon (Jun-Sep) when clouds block satellite observations.

**Mitigation:**
- Use quality flags to filter valid observations
- Apply cloud fraction thresholds (< 30% recommended)
- Use monthly composites to fill temporal gaps

### 2.4 Spatial Resolution Constraints

**Limitation:** ~1 km resolution (Level-3) may not capture fine-scale pollution gradients.

**Impact:**
- Cannot resolve pollution at street level
- May miss small-scale hotspots (e.g., individual industrial facilities)
- Smooths out sharp pollution gradients

**Example:** A small industrial area might be averaged with surrounding cleaner areas, reducing its apparent impact.

**Mitigation:**
- Use for regional and city-scale analysis, not micro-scale
- Combine with high-resolution models or ground measurements for local studies
- Focus on relative patterns rather than absolute point values

### 2.5 Overpass Time and Diurnal Variations

**Limitation:** Overpass at ~13:30 local time may not represent daily average conditions.

**Impact:**
- Midday conditions may differ from daily average
- Photochemical processes (e.g., O₃ formation) are time-dependent
- Some pollutants have strong diurnal cycles

**Example:** NO₂ photolyzes during the day, so midday measurements may underestimate daily average.

**Mitigation:**
- Acknowledge time-of-day bias in interpretations
- Use for relative comparisons rather than absolute values
- Combine with models that account for diurnal variations

### 2.6 Quality and Validation Challenges

**Limitation:** Satellite retrievals require validation against ground truth.

**Impact:**
- Retrieval algorithms have uncertainties
- Quality varies by pollutant and conditions
- Limited ground-based validation data in Delhi

**Mitigation:**
- Use quality flags (qa_value > 0.5 recommended)
- Validate against available ground stations
- Report uncertainties in analysis

---

## 3. Recommendations for Using Sentinel-5P in Delhi

### 3.1 Best Use Cases

1. **Regional Transport Analysis**
   - Excellent for tracking pollution from Punjab/Haryana crop burning
   - Identify upwind source regions
   - Map transport pathways

2. **Seasonal Pattern Analysis**
   - Strong for identifying seasonal trends
   - Detect extreme events (Diwali, crop burning)
   - Long-term trend monitoring

3. **Source Attribution**
   - Multi-pollutant analysis enables source identification
   - Distinguish traffic (NO₂) vs. power plants (SO₂) vs. biomass (CO)
   - Map industrial vs. residential patterns

4. **Policy Support**
   - Evaluate effectiveness of pollution control measures
   - Identify priority areas for intervention
   - Monitor compliance with air quality standards

### 3.2 Limitations to Acknowledge

1. **Not for Real-Time Monitoring**
   - Use ground-based sensors for immediate alerts
   - Satellite data best for trends and patterns

2. **Not for Micro-Scale Analysis**
   - Use for city/regional scale, not street-level
   - Combine with models for local predictions

3. **Requires Complementary Data**
   - Ground measurements for validation
   - Meteorological data for interpretation
   - Emission inventories for source attribution

### 3.3 Integration with Other Data Sources

**Recommended Approach:**
- **Satellite data:** Regional patterns, transport, trends
- **Ground stations:** Surface concentrations, real-time monitoring
- **Models:** Diurnal variations, forecasts, source apportionment
- **Emission inventories:** Source identification, policy evaluation

---

## 4. Key Findings from This Study

### 4.1 Pollution Regime Classification

- **62.5% of months:** Local pollution dominant (low wind conditions)
- **37.5% of months:** Advected pollution dominant (regional transport)
- **Finding:** Delhi's pollution is a mix of local and regional sources

### 4.2 Source Attribution

- **Severe episodes:** Often associated with transport from:
  - Northwest (Punjab/Haryana crop burning)
  - West (Industrial regions)
  - Local accumulation during calm conditions

### 4.3 Seasonal Patterns

- **Winter:** Elevated NO₂, SO₂ (heating, power generation)
- **Post-monsoon:** Peak CO, HCHO (crop burning)
- **Summer:** Moderate levels with regional transport
- **Monsoon:** Limited data due to clouds

### 4.4 Policy Implications

1. **Local Sources Matter:** 62.5% of time, pollution is locally generated
   - Need to address Delhi's own emissions (traffic, industry, power)

2. **Regional Transport Significant:** 37.5% of time, pollution is transported
   - Need coordinated action with neighboring states
   - Focus on crop burning management in Punjab/Haryana

3. **Multi-Pollutant Approach:** Different pollutants show different patterns
   - NO₂: Traffic and industry (local)
   - SO₂: Power plants (local + regional)
   - CO: Biomass burning (regional transport)
   - HCHO: Secondary formation (both)

---

## 5. Conclusions

Sentinel-5P TROPOMI data is a **valuable tool** for Delhi air quality studies, particularly for:
- Regional transport analysis
- Seasonal pattern identification
- Source attribution
- Long-term trend monitoring

However, it should be used **in combination with**:
- Ground-based measurements (for surface concentrations)
- Meteorological data (for interpretation)
- Emission inventories (for source identification)
- Air quality models (for forecasting)

**Key Message:** Satellite data provides the "big picture" of air quality, while ground measurements provide the "local details." Together, they enable comprehensive air quality management.

---

## 6. References and Further Reading

1. **Sentinel-5P Handbook:** https://sentinel.esa.int/web/sentinel/user-guides/sentinel-5p-handbook
2. **Copernicus Data Space:** https://dataspace.copernicus.eu/
3. **Google Earth Engine:** https://earthengine.google.com/
4. **ERA5 Reanalysis:** https://confluence.ecmwf.int/display/CKB/ERA5

---

**Authors:** Jakub Sumara, Zuzanna Słobodzian  
**Date:** January 2025  
**Project:** Sentinel-5P Air Pollution Dynamics over Delhi (AGH ML4SA2)
