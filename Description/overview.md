# Flood Path Detection Project Overview

Welcome to the documentation for the Flood Path Detection project, developed for the Mission Accepted Space Hackathon, October 26, 2025. This project leverages Canadian satellite data to predict flood paths for shoreline protection.

## Summary
The Flood Path Detection model uses a hybrid CNN + Random Forest approach to process RADARSAT-2/RCM SAR imagery, SCISAT moisture profiles, and CDEM elevation data, supplemented by NOAA eTRaP forecasts. It aims to provide real-time flood path predictions, reducing damages from events like the 2023 flood in Nova Scotia.

# Team Info

## Team Name
FLOW - Flood Observation and Warning

## Members
- Afif Asad Ruddraw (af411984@dal.ca)
- Ariyan Pancholia (ar748970@dal.ca)
- Akash Maity (ak298902@dal.ca)


## Acknowledgments
Thanks to ShiftKey Labs for organizing this hackathon, and to our mentors from MDA Space and the Canadian Space Agency (CSA) for their invaluable guidance and support.

# Datasets

## Satellite and Data Inputs
- **RADARSAT-2/RCM (CSA)**: 5-50m SAR Imagery (4-hr revisit) for flood detection.
- **SCISAT (CSA)**: Atmospheric moisture profiles for rainfall adjustment.
- **CDEM (NRCan)**: 1m LiDAR Elevation Data for flow direction.
- **NOAA eTRaP (NOAA)**: Rainfall Forecasts (0-24hr) for supplementary predictions.

## License and Usage Terms
- CSA data (RADARSAT-2/RCM, SCISAT, CDEM) is sourced from the Earth Observation Data Management System (EODMS) under the [Government of Canada Open Data License](https://open.canada.ca/en/open-government-licence-canada).
- NOAA eTRaP data is used under the [NOAA Public Data Access Policy](https://www.noaa.gov/organization/information-technology/policy-and-standards).
- All data is public, non-sensitive, and complies with hackathon guidelines.

# Technical Architecture

## Model Overview
The Flood Path detector uses a hybrid AI/ML model: a Convolutional Neural Network (CNN) for spatial analysis and Random Forest for feature classification to predict flood paths.

## Why This Model?
- CNN captures water edge patterns from RCM SAR effectively.
- Random Forest handles CDEM slopes and SCISAT moisture with high accuracy.
- Selected for 70%+ validation performance and RCM’s 4-hr real-time capability.

## Path Calculation
- CNN identifies flood seeds from RCM SAR, trained on generic flood extents.
- Random Forest simulates flow using CDEM gradients and SCISAT moisture.
- Fused output (60% CNN, 40% RF) generates a GeoJSON path.

# Results

## Prototype Status
- This is a prototype concept, presented as an idea for the Mission Accepted Space Hackathon, October 26, 2025.
- No real-world results are available; this documentation reflects simulated potential based on design.

## Simulated Outcomes
- The hybrid CNN + Random Forest model, using RADARSAT-2/RCM SAR, SCISAT moisture, and CDEM elevation data, is designed to predict flood paths.
- Theoretical accuracy is targeted at ~70% based on generic flood pattern assumptions, with RCM’s 4-hour revisit enabling near-real-time processing.
- A sample  path output is planned for frontend visualization, demonstrating the concept’s feasibility.

## Limitations
- Performance is untested; results depend on future data integration and validation.
- Cloud cover and data gaps (mitigated by SAR) require further exploration.


# Future Work

## Planned Enhancements
- Integrate NOAA eTRaP forecasts more robustly for 24-48hr predictions.
- Expand training with additional historical flood events from EODMS.
- Partner with CSA for real-time RCM data feeds to improve responsiveness.
- Develop a mobile alert system for the residents.

## Long-Term Vision
Scale to every other Canadian coastal cities, leveraging national EO assets for climate resilience.
