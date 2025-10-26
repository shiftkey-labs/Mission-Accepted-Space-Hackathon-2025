# Bloomwatch

A comprehensive platform for detecting and monitoring harmful algal blooms (HABs) using satellite imagery, designed to assist environmental agencies like the Department of Natural Resources (DNR) personnel in coastal management and mitigation efforts.

## Project Overview

This project provides an integrated solution for identifying algal blooms from satellite imagery and recommending optimal coastal locations for deploying mitigation measures. The system processes satellite data, detects algal blooms, and presents actionable insights through an intuitive user interface.

### Key Features

- **Satellite Image Processing**: Automated pipeline for ingesting and processing satellite imagery
- **Algal Bloom Detection**: Computer vision analysis to identify and map bloom locations
- **Coastal Recommendations**: Intelligent system for suggesting optimal mitigation deployment sites
- **User-Friendly Interface**: Modern frontend UI for DNR personnel to visualize and interact with bloom data

## Datasets

### Sentinel Hub

The project utilizes satellite imagery from **Sentinel Hub**, accessed through their API:

- **Authentication**: Token-based authentication (see flask_app/.env)
- **Coverage**: Multi-spectral satellite imagery for coastal monitoring
- **Resolution**: High-resolution imagery suitable for bloom detection

### Copernicus Data Space

Additional data sources from **Copernicus Data Space Ecosystem (CDSE)**:

- **API Access**: Integrated via `COPERNICUS_TOKEN` in [`flask_app/.env`](flask_app/.env)
- **Data Types**: Complementary satellite data for enhanced detection accuracy

## Architecture

### Backend

- **Framework**: Flask-based API (flask_app/)
- **Authentication Module**: Secure API access management (flask_app/app/auth/)
- **Main Application**: Core processing logic (flask_app/app/main/)

### Data Pipeline

1. **Satellite Image Acquisition**: Fetch imagery from Sentinel Hub and Copernicus APIs
2. **Image Processing**: Format and prepare satellite data for analysis
3. **Detection**: ML vision model processes imagery to identify algal blooms
4. **Analysis**: Generate coastal indicators and recommend deployment locations

### API Structure

```
algae_map_api/          # API endpoints and services
flask_app/              # Flask application
  ├── .env              # Environment variables and API tokens
  └── app/
      ├── auth/         # Authentication handlers
      └── main/         # Main application logic
```

## Results

The system successfully:

- Processes satellite imagery from multiple sources
- Provides real-time bloom detection capabilities
- Generates actionable coastal recommendations for DNR personnel
- Delivers insights through an accessible web interface

## Future Work

### Machine Learning Enhancement

- **Advanced Detection Models**: Implement deep learning models (CNN/Vision Transformers) for improved bloom identification
- **Multi-spectral Analysis**: Leverage additional spectral bands for enhanced accuracy
- **Bloom Classification**: Distinguish between different types of algal blooms
- **Severity Assessment**: Quantify bloom intensity and predict growth patterns

### Historical Data Platform

- **Time-series Analysis**: Track bloom patterns over months and years
- **Predictive Analytics**: Forecast bloom likelihood based on historical trends
- **Seasonal Modeling**: Identify seasonal patterns and high-risk periods
- **Data Visualization**: Interactive historical maps and trend analysis
- **Impact Assessment**: Correlate bloom events with environmental and economic impacts

### Additional Enhancements

- Real-time alerting system for new bloom detections
- Mobile application for field personnel
- Integration with water quality sensors
- Automated reporting and documentation

## Team

**Made by:**

- **Lennart Schaeffer**
- **Saul Hafting**
- **Xander Brown**

---

_Developed during the MDA Space Hackathon_

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- API tokens for Sentinel Hub and Copernicus (configured in flask_app/.env)

### Installation

```sh
cd flask_app
pip install -r requirements.txt
```

### Running the Application

```sh
cd flask_app
flask run
```

## Acknowledgments

- Sentinel Hub for satellite imagery access
- Copernicus Data Space Ecosystem
- MDA Space Hackathon organizers
