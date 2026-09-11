# 🌪️ AI/ML Based Cyclone Detection, Tracking & Intensity Prediction System

> **Smart India Hackathon 2026 — SIH26070**

An AI/ML-based cyclone monitoring system designed to classify tropical cyclone intensity and forecast cyclone track and intensity using historical meteorological observations.

---

## 📌 Overview

Tropical cyclones are dynamic weather systems that can rapidly change their position, wind speed, and central pressure. Accurate and timely prediction of cyclone intensity and movement is critical for disaster preparedness and emergency response.

Our system uses machine learning and deep learning techniques to analyze historical cyclone observations and provide:

- 🌪️ Cyclone intensity classification
- 📍 Historical cyclone track visualization
- 🔮 6-hour, 12-hour, 18-hour and 24-hour forecasting
- 💨 Future wind-speed prediction
- 🌀 Future central-pressure prediction
- 📊 Model confidence and probability analysis
- 🗺️ Cyclone track visualization
- 📈 Model performance analytics

---

## 🎯 Problem Statement

### Smart India Hackathon 2026

**Problem Statement ID:** SIH26070

**Organization:** Ministry of Earth Sciences (MoES)

The challenge is to develop an AI/ML-based system capable of identifying, classifying and predicting tropical cyclone patterns using meteorological and multi-source observations.

Cyclones can cause:

- Extremely strong winds
- Heavy rainfall
- Storm surges
- Coastal flooding
- Infrastructure damage
- Transportation and communication disruption
- Loss of life and property

Because cyclone characteristics continuously change, timely prediction of their intensity and movement is a challenging problem.

---

# 💡 Our Solution

Our approach combines **XGBoost** and **PyTorch BiLSTM with Self-Attention** to create an AI-based cyclone analysis and forecasting pipeline.

### System Pipeline

```text
NOAA IBTrACS Historical Data
            ↓
     Data Preprocessing
            ↓
     Feature Engineering
            ↓
   ┌────────┴─────────┐
   ↓                  ↓
 XGBoost            PyTorch
Classifier           BiLSTM
   +               + Self-Attention
   ↓                  ↓
IMD Intensity      Track & Intensity
Classification       Forecasting
   └────────┬─────────┘
            ↓
       FastAPI Backend
            ↓
     Web Dashboard
