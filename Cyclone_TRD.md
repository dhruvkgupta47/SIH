# Technical Requirements Document (TRD)
## AI-Based Cyclone Tracking & Intensity Prediction System

**Smart India Hackathon 2026 — SIH26070**  
**Organization:** Ministry of Earth Sciences (MoES)  
**Team:** Code Before Coffee**

---

## 1. Technical Architecture

```text
NOAA IBTrACS
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
 ┌──────────────┬──────────────────┐
 ↓              ↓
XGBoost       PyTorch
Classifier    BiLSTM + Self-Attention
 ↓              ↓
IMD            Track + Intensity
Intensity      Forecasting
 ↓              ↓
 └───────┬──────┘
         ↓
      FastAPI
         ↓
      Frontend
```

---

## 2. Technology Stack

| Layer | Technology |
|---|---|
| Programming | Python |
| Numerical Computing | NumPy |
| Data Processing | Pandas |
| Data Retrieval | Requests |
| Data Source | NOAA IBTrACS |
| Classification | XGBoost |
| Deep Learning | PyTorch |
| ML Utilities | Scikit-learn |
| Forecasting | BiLSTM |
| Attention | Self-Attention |
| Backend | FastAPI |
| API Server | Uvicorn |
| Validation | Pydantic |
| Database | SQLite |
| API Format | REST / JSON |
| Current Deployment | Local / On-Premise |

---

## 3. Data Source

The current prototype primarily uses **NOAA IBTrACS (International Best Track Archive for Climate Stewardship)** historical cyclone observations, particularly North Indian Ocean cyclone data.

The data contains historical observations such as:
- Storm identity
- Timestamp
- Latitude
- Longitude
- Wind speed
- Central pressure
- Intensity information

---

## 4. Data Processing Pipeline

```text
Raw IBTrACS Data
       ↓
Data Cleaning
       ↓
Missing Value Handling
       ↓
Track Processing
       ↓
Feature Engineering
       ↓
Model-Ready Dataset
```

---

## 5. Feature Engineering

### Physical Features
- Wind speed
- Central pressure
- Latitude
- Longitude

### Movement Features
- Translational speed
- Heading
- Latitude rate
- Longitude rate

### Temporal Features
- Wind change per hour
- Pressure change per hour
- Storm age

### Derived Features
- Coriolis proxy
- Wind/pressure ratio
- Day-of-year sine
- Day-of-year cosine

---

## 6. XGBoost Classifier

### Purpose

The XGBoost model performs multi-class cyclone intensity classification.

```text
Meteorological Features
          ↓
     Preprocessing
          ↓
       XGBoost
          ↓
    Multi-Class Output
          ↓
      IMD Category
```

### Classifier Variants

```text
classifier_full
classifier_indirect
```

The API selects the appropriate classifier depending on the available input information.

### Classification Output

- Category
- Abbreviation
- Severity index
- Confidence
- Category probabilities
- Model type
- Model variant

---

## 7. Classification API

### Endpoint

```http
POST /classify
```

### Example Request

```json
{
  "wind_knots": 40,
  "pressure_hpa": 994,
  "latitude": 14.0,
  "longitude": 82.0,
  "translational_speed_kmh": 15,
  "heading_deg": 270
}
```

---

## 8. BiLSTM + Self-Attention Forecaster

The forecasting model treats cyclone behavior as a sequential time-series problem.

```text
Historical Track Sequence
          ↓
     Feature Scaling
          ↓
      BiLSTM
          ↓
   Self-Attention
          ↓
 Prediction Layers
          ↓
+6h → +12h → +18h → +24h
```

### Forecast Outputs

For each horizon:
- Latitude
- Longitude
- Wind speed
- Central pressure
- Intensity category

---

## 9. Forecast Input

Historical track observations contain:

- Latitude
- Longitude
- Wind speed
- Pressure
- Translational speed
- Heading
- Wind change
- Pressure change

The API is designed around an expected lookback of **8 observations** and pads or trims the supplied sequence to the required length.

---

## 10. Forecast API

### Endpoint

```http
POST /forecast
```

### Output Structure

Each prediction contains:
- Horizon hours
- Latitude
- Longitude
- Wind speed
- Pressure
- Intensity category
- Color

Forecast horizons:
- 6 hours
- 12 hours
- 18 hours
- 24 hours

---

## 11. Database Architecture

Current database:

```text
SQLite
   │
   ├── storms
   ├── track_points
   ├── model_runs
   └── predictions
```

### storms
Stores cyclone-level information.

### track_points
Stores historical cyclone observations.

### model_runs
Stores model metadata and evaluation information.

### predictions
Stores forecast-related information.

---

## 12. Backend Architecture

FastAPI provides the REST service layer.

```text
                 FastAPI
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
  /classify     /forecast    /cyclones
       │            │            │
       ↓            ↓            ↓
   XGBoost       BiLSTM       SQLite
```

Additional endpoints:

```http
GET /cyclones/{storm_id}
GET /models
GET /health
```

---

## 13. API Validation

Pydantic validates API requests.

Current validation ranges include:

```text
Pressure: 800–1050 hPa
Latitude: -40–40
Longitude: 30–120
Heading: 0–360°
Wind: 0–300 knots
```

---

## 14. Model Storage

```text
models/
│
├── classifier_full.joblib
├── classifier_indirect.joblib
├── forecaster.pt
└── forecaster_scalers.joblib
```

- XGBoost classifiers are stored using Joblib.
- The BiLSTM forecaster is stored as a PyTorch model.
- Forecast scalers are stored separately.

---

## 15. API Health Monitoring

### Endpoint

```http
GET /health
```

The response can report:
- API status
- Full classifier status
- Indirect classifier status
- Forecaster status
- Database status
- Track point count
- Storm count

---

## 16. Frontend Integration

The frontend communicates with the backend through HTTP/JSON.

```text
Frontend
   │
   │ HTTP / JSON
   ▼
FastAPI
   │
   ├── XGBoost
   ├── BiLSTM
   └── SQLite
```

The frontend should not directly load:
- `.joblib`
- `.pt`
- `.db`

Instead:

```text
Frontend → FastAPI → Model/Database → JSON Response → Frontend
```

---

## 17. Security Requirements

For the current prototype:
- Validate all API inputs.
- Do not expose model files directly.
- Do not expose database credentials.
- Keep configuration separate from source code.

For production:
- Restrict CORS origins.
- Add authentication and authorization where required.
- Use HTTPS.
- Protect database and model storage.

---

## 18. Deployment

### Current Deployment

```text
Windows/Linux
      ↓
Python Environment
      ↓
Uvicorn
      ↓
FastAPI :8000
```

Run:

```bash
python run.py --api-only
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## 19. Testing Requirements

### Unit Testing

Test:
- Feature engineering
- IMD category rules
- XGBoost classifier
- BiLSTM forecaster
- Database operations
- API validation

### API Testing

```text
POST /classify
POST /forecast
GET /cyclones
GET /cyclones/{id}
GET /models
GET /health
```

### ML Evaluation

Classification:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

Forecasting:
- Latitude error
- Longitude error
- Wind error
- Pressure error
- Horizon-wise error

---

## 20. Technical Risks

| Risk | Mitigation |
|---|---|
| Missing meteorological values | Appropriate classifier variant and preprocessing |
| Invalid API inputs | Pydantic validation |
| Forecast uncertainty | Clearly label outputs as AI forecasts |
| Historical data bias | Expand dataset in future |
| Model overfitting | Cross-validation and independent testing |
| Database scalability | Future PostgreSQL/PostGIS migration |
| Lack of real-time data | Integrate operational feeds in future |

---

## 21. Current vs Future Architecture

### Currently Implemented

```text
NOAA IBTrACS
      ↓
Python / Pandas / NumPy
      ↓
Feature Engineering
      ↓
XGBoost
      ↓
IMD Intensity Classification
      ↓
PyTorch BiLSTM + Self-Attention
      ↓
6–24h Forecast
      ↓
FastAPI
      ↓
Dashboard
```

### Future Extension

```text
INSAT-3D/3DR
      ↓
Satellite Image Processing
      ↓
Image-Based Detection Model
      ↓
Cyclone Detection
      ↓
XGBoost
      ↓
Intensity
      ↓
BiLSTM + Attention
      ↓
Track Forecast
```

The satellite-image layer is a future extension and should not be presented as currently implemented.

---

## 22. Technical Explanation for Judges

> Our current architecture has two AI components. First, we use XGBoost for multi-class cyclone intensity classification using structured meteorological features such as wind speed, central pressure, location and temporal changes. Second, we use a PyTorch Bidirectional LSTM with Self-Attention to learn the sequential behavior of cyclone tracks and forecast latitude, longitude, wind speed and pressure at 6, 12, 18 and 24-hour horizons. Both models are exposed through a FastAPI backend, while historical cyclone data is maintained in SQLite and sourced primarily from NOAA IBTrACS. The frontend consumes these APIs to visualize cyclone tracks, intensity and forecasts.

---

## 23. Disclaimer

This is an academic and hackathon prototype. Forecast outputs are intended for research and demonstration and should not replace official forecasts or warnings issued by authorized meteorological agencies.
