# 🔍 PPT vs Codebase — Technology Mismatch Report

I compared **every technology from your 3 presentation slides** against what's **actually in your code**. Here's the full audit:

---

## ❌ Technologies in PPT but NOT in Your Code (10 Mismatches)

| # | Technology (from PPT) | PPT Section | Status in Code | Risk Level |
|---|---|---|---|---|
| 1 | **TensorFlow / Keras** | ML/DL Frameworks | ❌ **Not used at all.** Your entire ML stack is PyTorch. Zero TF imports anywhere. | 🔴 HIGH — Judges may ask "show me where you use Keras" |
| 2 | **Flask** | Backend | ❌ **Not used.** Backend is 100% FastAPI + Uvicorn. No Flask anywhere. | 🔴 HIGH — Very easy for judges to notice |
| 3 | **Node.js** | Backend | ❌ **Not used.** No `package.json`, no `node_modules`, no JS backend code. | 🔴 HIGH — Entirely absent |
| 4 | **ConvLSTM** | Track/Intensity Prediction | ⚠️ **Not implemented.** Your [forecaster.py](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/forecaster.py) uses **BiLSTM** (Bidirectional LSTM), not ConvLSTM. These are different architectures. | 🟡 MEDIUM — ConvLSTM has 2D convolution layers; yours is pure sequential LSTM |
| 5 | **GDAL** | Libraries & Tools | ❌ **Not installed.** Not in [requirements.txt](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/requirements.txt), no `import gdal` or `from osgeo` anywhere. | 🟡 MEDIUM — Not critical but listed prominently |
| 6 | **InfluxDB** | Database & Storage | ⚠️ **Only export format exists.** [database.py L409-433](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/database.py#L409-L433) has a `to_influx_line_protocol()` method, but there's no InfluxDB server, no InfluxDB client library, and no actual InfluxDB connection. | 🟡 MEDIUM — Export function exists but no actual DB |
| 7 | **Amazon S3** | Database & Storage | ❌ **Not used.** No `boto3`, no S3 bucket config, no object storage code. | 🟡 MEDIUM |
| 8 | **AWS** | Deployment | ⚠️ **Not configured.** Only mentioned in a Dockerfile comment. No AWS-specific deployment files (no ECS/EKS/Lambda config). | 🟢 LOW — Dockerfile is compatible, just not set up |
| 9 | **Google Cloud** | Deployment | ⚠️ **Not configured.** Same as AWS — only a comment. No `app.yaml` or Cloud Run config. | 🟢 LOW |
| 10 | **ChatGPT (OpenAI)** | AI Assistant | ❌ **Not integrated.** No OpenAI API key, no `openai` library, no code referencing it. | 🟢 LOW — PPT lists it as a dev tool, not a system component |

---

## ✅ Technologies in PPT that ARE Properly Matched (21/31)

| Technology | PPT Section | Where in Code | Status |
|---|---|---|---|
| **Python** | Libraries & Tools | Every `.py` file | ✅ Perfect |
| **NumPy** | Libraries & Tools | `requirements.txt`, all ML modules | ✅ Perfect |
| **xarray** | Libraries & Tools | `requirements.txt` | ✅ Installed |
| **PyTorch** | ML/DL Frameworks | `classifier_cnn.py`, `forecaster_transformer.py`, `forecaster.py` | ✅ Perfect |
| **CNN (ResNet)** | Detection/Classification | [classifier_cnn.py](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/classifier_cnn.py) — `ResNet-18` backbone | ✅ Perfect |
| **EfficientNet** | Detection/Classification | [classifier_cnn.py L103](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/classifier_cnn.py#L103) — `EfficientNet-B0` alternative | ✅ Perfect |
| **Transformer** | Track/Intensity Prediction | [forecaster_transformer.py](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/forecaster_transformer.py) — Spatiotemporal Transformer | ✅ Perfect |
| **FastAPI** | Backend | [api.py](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/api.py) — 6 REST endpoints | ✅ Perfect |
| **PostgreSQL** | Database | [docker-compose.yml](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/docker-compose.yml) — PostgreSQL 16 | ✅ Perfect |
| **PostGIS** | Database | [docker-compose.yml](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/docker-compose.yml) — `postgis/postgis:16-3.4` | ✅ Perfect |
| **Kaggle** | Data Sources | Listed as data source in PPT (not an integrated tool) | ✅ OK |
| **React** | Frontend | [FRONTEND_GUIDE.md](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/FRONTEND_GUIDE.md) — planned but **no `frontend/` folder exists yet** | ⚠️ Guide only |
| **Leaflet.js** | Frontend | [dashboard.py L22](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/dashboard.py#L22) — embedded in HTML dashboard | ✅ Perfect |
| **Mapbox GL JS** | Frontend | [FRONTEND_GUIDE.md](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/FRONTEND_GUIDE.md) — listed as option, **not actually used** in dashboard | ⚠️ Guide only |
| **Docker** | Deployment | [Dockerfile](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/Dockerfile) + [docker-compose.yml](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/docker-compose.yml) | ✅ Perfect |
| **On-Prem Deployment** | Deployment | `docker compose up` for local demo | ✅ Perfect |
| **INSAT-3D/3DR** | Data Sources | [data_loader.py](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/data_loader.py) — `generate_insat_thermal_grid()` | ✅ Simulated |
| **IBTrACS** | Data Sources | [data_loader.py L46-50](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/data_loader.py#L46-L50) — downloads from NOAA | ✅ Perfect |
| **IMD Archives** | Data Sources | IMD classification rules in [imd_rules.py](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/imd_rules.py) | ✅ Perfect |
| **ERA5** | Data Sources | `xarray` in requirements (ready to use) | ⚠️ Ready, not active |
| **XGBoost** | ML (implicit in classifier) | [classifier.py](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/src/classifier.py), [requirements.txt](file:///c:/Users/DHURV%20GUPTA/OneDrive/Desktop/SIH/requirements.txt) | ✅ Perfect |

---

## 🎯 Summary: What to Fix in Your PPT

> [!CAUTION]
> **3 technologies are serious mismatches** that judges could catch easily:

### 🔴 Must Fix (Remove or Replace in PPT)

| PPT Says | Reality | Recommendation |
|---|---|---|
| **TensorFlow / Keras** | You only use **PyTorch** | Remove TF/Keras. Your PPT slide 5 already has a red ❌ on it — make sure it's clearly crossed out or removed entirely |
| **Flask** | You only use **FastAPI** | Remove Flask from the Backend section |
| **Node.js** | No JavaScript backend at all | Remove Node.js from the Backend section |

### 🟡 Should Fix (Clarify in PPT)

| PPT Says | Reality | Recommendation |
|---|---|---|
| **ConvLSTM** | You use **BiLSTM** (no 2D convolution) | Change to "BiLSTM" or "LSTM" in the PPT. ConvLSTM is a specific architecture with Conv2D layers — yours doesn't have that |
| **GDAL** | Not installed or imported | Either add `gdal` to your requirements.txt and use it, or remove from PPT |
| **InfluxDB** | Only an export function, no actual database | Either clarify as "InfluxDB-compatible export" or remove |
| **Amazon S3** | No S3 integration | Remove unless you plan to add `boto3` |

### 🟢 Minor (OK to Keep)

| PPT Says | Reality | Recommendation |
|---|---|---|
| **AWS / Google Cloud** | Dockerfile is compatible but not deployed | OK — Dockerfile comment says "Compatible with AWS, GCP". Defensible |
| **ChatGPT (OpenAI)** | Development assistance tool, not system integration | OK — PPT labels it as "AI Assistant" for dev, not a product feature |
| **React / Mapbox GL JS** | Guide exists, no `frontend/` folder built yet | OK if you plan to build it before presentation |
