# Product Requirements Document (PRD)
## AI-Based Cyclone Tracking & Intensity Prediction System

**Smart India Hackathon 2026 — SIH26070**  
**Organization:** Ministry of Earth Sciences (MoES)  
**Team:** Code Before Coffee  
**Institute:** Swami Keshvanand Institute of Technology, Jaipur

---

## 1. Product Overview

The system is an AI-powered cyclone monitoring and prediction platform that analyzes historical meteorological cyclone observations to classify cyclone intensity and forecast cyclone track and intensity.

The current prototype uses:
- **XGBoost** for cyclone intensity classification.
- **PyTorch BiLSTM with Self-Attention** for sequential track and intensity forecasting.
- **FastAPI** for exposing the AI functionality.
- **SQLite** for historical cyclone data and system information.

---

## 2. Problem Statement

Tropical cyclones are highly dynamic systems whose location, wind speed, central pressure, direction of movement, and intensity can change continuously.

Cyclones can cause:
- High-speed winds
- Heavy rainfall
- Storm surges
- Coastal flooding
- Infrastructure damage
- Transportation and communication disruption
- Loss of life and property

Traditional analysis requires continuous observation and expert interpretation. Processing large amounts of cyclone information quickly is therefore challenging.

The product aims to answer two key questions:

> **How strong is the cyclone now?**

> **Where is the cyclone likely to move and how will its intensity change?**

---

## 3. Product Goals

### Primary Goals

1. Automatically classify cyclone intensity.
2. Forecast cyclone movement for the next 24 hours.
3. Forecast future wind speed and central pressure.
4. Predict future cyclone intensity.
5. Visualize observed and predicted cyclone tracks.
6. Provide model confidence and probability information.
7. Provide model performance analytics.

### Secondary Goals

- Reduce manual processing of cyclone observations.
- Provide an additional AI-based decision-support tool.
- Maintain an architecture that can later support real-time data.

---

## 4. Target Users

### Meteorologists
Analyze cyclone evolution and AI predictions.

### Disaster Management Authorities
Use cyclone predictions as additional decision-support information.

### Researchers
Study historical cyclone behavior and model performance.

### Academic Users
Learn and experiment with AI-based cyclone prediction.

---

## 5. Core Product Features

### 5.1 Historical Cyclone Database

The system provides historical cyclone information including:
- Storm ID
- Storm name
- Season
- Maximum wind
- Minimum pressure
- Peak intensity category
- Historical track points

### 5.2 AI Intensity Classification

The system accepts meteorological parameters and predicts an IMD cyclone intensity category.

Inputs may include:
- Wind speed
- Central pressure
- Latitude
- Longitude
- Translational speed
- Heading
- Wind-speed change
- Pressure change
- Storm age
- Derived meteorological features

Outputs include:
- Predicted category
- Abbreviation
- Severity index
- Confidence
- Probability distribution
- Model variant

### 5.3 Track & Intensity Forecasting

The system forecasts cyclone evolution at:
- +6 hours
- +12 hours
- +18 hours
- +24 hours

Forecast outputs:
- Latitude
- Longitude
- Wind speed
- Central pressure
- Intensity category

### 5.4 Cyclone Map

The interface should show:
- Observed cyclone track
- Current position
- AI forecast track
- Future forecast points

### 5.5 Analytics

The product provides:
- Classification performance
- Confusion matrices
- Feature importance
- Forecast metrics
- Training curves
- Track plots

### 5.6 System Health

The dashboard can show:
- API status
- Database status
- Classifier status
- Forecaster status
- Number of cyclone records
- Number of track points

---

## 6. IMD Intensity Categories

The system supports eight categories:

1. Low Pressure Area
2. Depression
3. Deep Depression
4. Cyclonic Storm
5. Severe Cyclonic Storm
6. Very Severe Cyclonic Storm
7. Extremely Severe Cyclonic Storm
8. Super Cyclonic Storm

---

## 7. User Flow

```text
Open Dashboard
      ↓
Select Historical Cyclone
      ↓
View Observed Track
      ↓
Analyze Current Conditions
      ↓
XGBoost Intensity Classification
      ↓
View Category + Confidence
      ↓
Submit Historical Sequence
      ↓
BiLSTM + Self-Attention Forecast
      ↓
View +6/+12/+18/+24h Forecast
      ↓
Compare Observed vs AI Forecast
```

---

## 8. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Retrieve historical cyclone records |
| FR-02 | Display cyclone details |
| FR-03 | Display historical cyclone tracks |
| FR-04 | Classify cyclone intensity |
| FR-05 | Provide classification confidence |
| FR-06 | Provide category probabilities |
| FR-07 | Forecast cyclone track |
| FR-08 | Forecast wind speed |
| FR-09 | Forecast central pressure |
| FR-10 | Forecast future intensity category |
| FR-11 | Provide 6–24 hour forecasts |
| FR-12 | Visualize observed and predicted tracks |
| FR-13 | Display model analytics |
| FR-14 | Display system health |
| FR-15 | Expose prediction functionality through REST APIs |

---

## 9. Non-Functional Requirements

### Performance
- Prediction requests should return within a reasonable response time.
- Models should be loaded once rather than retrained for every prediction.

### Reliability
- Invalid inputs should be rejected.
- API errors should provide meaningful responses.

### Usability
- Dashboard should present cyclone information clearly.
- Forecasts should be visually distinguishable from observed data.

### Maintainability
- Data processing, models, database, and API should remain modular.

### Scalability
The system should allow future migration from:
- SQLite to PostgreSQL/PostGIS
- Local deployment to Docker/cloud infrastructure

---

## 10. Success Metrics

### Classification
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

### Forecasting
- Latitude error
- Longitude error
- Wind-speed error
- Pressure error
- Error at each forecast horizon

### System
- API response time
- Successful request rate
- Model availability
- Database availability

---

## 11. Future Scope

Future versions may include:
- INSAT-3D/3DR satellite data
- Real-time meteorological feeds
- Satellite-image-based cyclone detection
- Advanced geospatial visualization
- Real-time alert generation
- PostgreSQL/PostGIS
- Docker deployment
- Cloud deployment
- Multi-basin support
- Automated model retraining

These are future extensions and should not be presented as currently implemented features.

---

## 12. Product Disclaimer

This is an academic and hackathon prototype. Its outputs are intended for research and demonstration and should not replace official warnings or forecasts issued by authorized meteorological agencies.
