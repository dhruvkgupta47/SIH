# SIH26070 — Frontend Development Guide
### React + Leaflet.js / Mapbox GL JS Integration with FastAPI Backend

This guide provides a step-by-step blueprint for building the operational frontend dashboard for the **Cyclone AI/ML System (SIH26070)** matching the official technologies:
- **Framework**: React (Vite)
- **Mapping**: Leaflet.js (`react-leaflet`) / Mapbox GL JS
- **Visuals**: Recharts / Chart.js for intensity timelines, Lucide icons for meteorological badges
- **Backend Connection**: FastAPI REST API running on `http://localhost:8000` (CORS already enabled for all origins)

---

## 1. Quick Project Scaffolding

From the project root (`e:\SIH`), run:

```bash
# 1. Initialize modern React app with Vite
npm create vite@latest frontend -- --template react

# 2. Enter directory and install dependencies
cd frontend
npm install

# 3. Install mapping, charting, and UI libraries
npm install leaflet react-leaflet recharts lucide-react axios
```

Add Leaflet CSS to `frontend/index.html` (inside `<head>`):
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
```

---

## 2. API Integration Layer (`frontend/src/services/api.js`)

Create `src/services/api.js` to communicate with the FastAPI backend:

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

export const getHealth = () => api.get('/health');
export const getCyclones = () => api.get('/cyclones');
export const getCycloneTrack = (stormId) => api.get(`/cyclones/${stormId}`);
export const getModelRuns = () => api.get('/models');

// 1. Classical / Tabular Intensity Classification (XGBoost)
export const classifyIntensity = (features) => api.post('/classify', features);

// 2. Multi-Source Satellite Classification (PyTorch ResNet-18 CNN)
export const classifySatellite = (data) => api.post('/classify-satellite', data);

// 3. Spatiotemporal Track & Intensity Forecasting (+6h to +24h)
export const forecastTrackTransformer = (trackHistory) => 
  api.post('/forecast-transformer', { track_history: trackHistory });

export default api;
```

---

## 3. Recommended Dashboard Layout

A winning SIH dashboard layout consists of 4 interactive panels:

```
+-----------------------------------------------------------------------------------+
|  HEADER: Cyclone AI Early Warning System | Live IMD Status Badge | Time UTC        |
+------------------------------------------+----------------------------------------+
|  LEFT PANEL (35% width)                  |  RIGHT PANEL (65% width)               |
|  1. Storm Selector Dropdown              |  1. Interactive Leaflet Map            |
|     (Amphan, Fani, Biparjoy, Live Feed)  |     - Historical Path (Blue Polyline)   |
|                                          |     - Current Eye Location (Pulsing)   |
|  2. Intensity & Detection Card           |     - Forecast Cone (Red/Orange Line)  |
|     - Category (e.g. ESCS / VSCS)        |     - IMD Color Markers (+6h..+24h)    |
|     - Severity Index (0 - 7)             |                                        |
|     - Wind Speed (kt / km/h)             |  2. Intensity Forecast Chart           |
|     - Central Pressure (hPa)             |     - Wind Speed Trajectory (+24h)     |
|     - Model: ResNet-18 / XGBoost         |     - Central Pressure Drop Curve      |
|                                          |                                        |
|  3. Evacuation & Disaster Alert Badge    |                                        |
+------------------------------------------+----------------------------------------+
```

---

## 4. Key Components Implementation

### Component A: Interactive Map (`src/components/CycloneMap.jsx`)

Renders the satellite track and forecasted trajectory cone:

```jsx
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// IMD Official Color Palette
const getCategoryColor = (category) => {
  if (category?.includes('Super')) return '#8B0000'; // Dark Red
  if (category?.includes('Extremely')) return '#FF0000'; // Red
  if (category?.includes('Very Severe')) return '#FF6600'; // Orange
  if (category?.includes('Severe')) return '#FFC000'; // Amber
  if (category?.includes('Cyclonic Storm')) return '#70AD47'; // Green
  if (category?.includes('Depression')) return '#2E75B6'; // Blue
  return '#A6A6A6'; // Grey
};

export default function CycloneMap({ trackPoints = [], forecastPoints = [] }) {
  const center = trackPoints.length > 0
    ? [trackPoints[trackPoints.length - 1].latitude, trackPoints[trackPoints.length - 1].longitude]
    : [15.0, 85.0]; // Bay of Bengal center

  const historyCoords = trackPoints.map(p => [p.latitude, p.longitude]);
  const forecastCoords = forecastPoints.map(p => [p.latitude, p.longitude]);
  const fullForecastLine = historyCoords.length > 0 
    ? [historyCoords[historyCoords.length - 1], ...forecastCoords] 
    : forecastCoords;

  return (
    <MapContainer center={center} zoom={5} style={{ height: '520px', width: '100%', borderRadius: '12px' }}>
      {/* Dark / Satellite tile layer */}
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        attribution='&copy; OpenStreetMap &copy; CARTO'
      />

      {/* Historical Track Line */}
      {historyCoords.length > 1 && (
        <Polyline positions={historyCoords} color="#2563eb" weight={4} opacity={0.8} />
      )}

      {/* Historical Points */}
      {trackPoints.map((pt, i) => (
        <CircleMarker
          key={`hist-${i}`}
          center={[pt.latitude, pt.longitude]}
          radius={4}
          color="#1e40af"
          fillColor="#3b82f6"
          fillOpacity={0.9}
        >
          <Popup>
            <strong>{pt.timestamp}</strong><br />
            Wind: {pt.wind_speed_kt} kt | Pres: {pt.pressure_mb} hPa<br />
            Category: {pt.intensity_category}
          </Popup>
        </CircleMarker>
      ))}

      {/* Forecasted Trajectory Cone (+6h to +24h) */}
      {forecastCoords.length > 0 && (
        <Polyline positions={fullForecastLine} color="#ef4444" weight={3} dashArray="8, 8" />
      )}

      {/* Forecast Points with IMD Colors */}
      {forecastPoints.map((pt, i) => (
        <CircleMarker
          key={`fcst-${i}`}
          center={[pt.latitude, pt.longitude]}
          radius={7}
          color="#000"
          fillColor={pt.color_hex || getCategoryColor(pt.intensity_category)}
          fillOpacity={1}
        >
          <Popup>
            <strong>+{pt.horizon_hours}h Forecast</strong><br />
            Category: <span style={{ color: pt.color_hex, fontWeight: 'bold' }}>{pt.intensity_category}</span><br />
            Wind: {pt.wind_knots} kt | Pres: {pt.pressure_hpa} hPa
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
```

---

### Component B: Intensity Alert Card (`src/components/IntensityCard.jsx`)

```jsx
import React from 'react';
import { AlertTriangle, Wind, Gauge, ShieldAlert } from 'lucide-react';

export default function IntensityCard({ classification }) {
  if (!classification) return <div>Select a storm to view classification...</div>;

  const { category, abbreviation, severity_index, confidence, color_hex, description, model_type } = classification;

  return (
    <div style={{
      borderLeft: `8px solid ${color_hex}`,
      backgroundColor: '#1e293b',
      color: '#f8fafc',
      padding: '20px',
      borderRadius: '8px',
      marginBottom: '16px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '1.25rem' }}>{category}</h3>
        <span style={{
          backgroundColor: color_hex,
          color: '#fff',
          padding: '4px 10px',
          borderRadius: '4px',
          fontWeight: 'bold'
        }}>
          {abbreviation} (Stage {severity_index}/7)
        </span>
      </div>

      <p style={{ color: '#94a3b8', margin: '8px 0 16px 0' }}>{description}</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
        <div style={{ background: '#0f172a', padding: '10px', borderRadius: '6px' }}>
          <small style={{ color: '#94a3b8' }}>Confidence</small>
          <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#38bdf8' }}>
            {(confidence * 100).toFixed(1)}%
          </div>
        </div>
        <div style={{ background: '#0f172a', padding: '10px', borderRadius: '6px' }}>
          <small style={{ color: '#94a3b8' }}>Model Architecture</small>
          <div style={{ fontSize: '0.9rem', fontWeight: 'bold', color: '#a78bfa' }}>
            {model_type}
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

### Component C: Forecast Trajectory Chart (`src/components/ForecastChart.jsx`)

```jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function ForecastChart({ forecastData = [] }) {
  const chartData = forecastData.map(p => ({
    horizon: `+${p.horizon_hours}h`,
    wind: p.wind_knots,
    pressure: p.pressure_hpa,
  }));

  return (
    <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', marginTop: '16px' }}>
      <h4 style={{ margin: '0 0 12px 0', color: '#f8fafc' }}>24-Hour Wind & Pressure Forecast</h4>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={chartData}>
          <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
          <XAxis dataKey="horizon" stroke="#94a3b8" />
          <YAxis yAxisId="left" stroke="#f87171" domain={['auto', 'auto']} label={{ value: 'Wind (kt)', angle: -90, position: 'insideLeft', fill: '#f87171' }} />
          <YAxis yAxisId="right" orientation="right" stroke="#38bdf8" domain={['auto', 'auto']} label={{ value: 'Pressure (hPa)', angle: 90, position: 'insideRight', fill: '#38bdf8' }} />
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
          <Line yAxisId="left" type="monotone" dataKey="wind" stroke="#ef4444" strokeWidth={3} name="Wind Speed (kt)" />
          <Line yAxisId="right" type="monotone" dataKey="pressure" stroke="#0ea5e9" strokeWidth={3} name="Central Pressure (hPa)" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

---

## 5. Main Dashboard Assembly (`frontend/src/App.jsx`)

```jsx
import React, { useEffect, useState } from 'react';
import CycloneMap from './components/CycloneMap';
import IntensityCard from './components/IntensityCard';
import ForecastChart from './components/ForecastChart';
import { getCyclones, getCycloneTrack, classifySatellite, forecastTrackTransformer } from './services/api';

export default function App() {
  const [cyclones, setCyclones] = useState([]);
  const [selectedStormId, setSelectedStormId] = useState('');
  const [trackPoints, setTrackPoints] = useState([]);
  const [forecastPoints, setForecastPoints] = useState([]);
  const [classification, setClassification] = useState(null);
  const [loading, setLoading] = useState(false);

  // 1. Fetch available benchmark cyclones on mount
  useEffect(() => {
    getCyclones().then(res => {
      setCyclones(res.data);
      if (res.data.length > 0) {
        setSelectedStormId(res.data[0].storm_id);
      }
    });
  }, []);

  // 2. When a storm is selected, load track and run AI inference
  useEffect(() => {
    if (!selectedStormId) return;
    setLoading(true);

    getCycloneTrack(selectedStormId).then(async (res) => {
      const track = res.data.track;
      setTrackPoints(track);

      const latest = track[track.length - 1];

      // A. Run ResNet-18 Fusion CNN Intensity Classifier
      const clfRes = await classifySatellite({
        latitude: latest.latitude,
        longitude: latest.longitude,
        wind_knots: latest.wind_speed_kt,
        pressure_hpa: latest.pressure_mb,
      });
      setClassification(clfRes.data);

      // B. Run Spatiotemporal Transformer Forecaster (+6h to +24h)
      const fcstRes = await forecastTrackTransformer(track.slice(-8));
      setForecastPoints(fcstRes.data.predictions);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [selectedStormId]);

  return (
    <div style={{ backgroundColor: '#0f172a', minHeight: '100vh', color: '#f8fafc', padding: '24px', fontFamily: 'Inter, sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#38bdf8' }}>
            CycloneAI — Spatiotemporal Tracking & Intensity System
          </h1>
          <small style={{ color: '#94a3b8' }}>Smart India Hackathon 2026 | Problem Statement SIH26070</small>
        </div>
        <select 
          value={selectedStormId} 
          onChange={(e) => setSelectedStormId(e.target.value)}
          style={{ background: '#1e293b', color: '#f8fafc', padding: '8px 16px', borderRadius: '6px', border: '1px solid #334155' }}
        >
          {cyclones.map(s => (
            <option key={s.storm_id} value={s.storm_id}>
              {s.name} ({s.season}) — Peak: {s.peak_category || 'Depression'}
            </option>
          ))}
        </select>
      </header>

      {loading && <div style={{ color: '#38bdf8', marginBottom: '12px' }}>Updating AI inference models...</div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px' }}>
        {/* Left Side: Prediction and Charts */}
        <div>
          <IntensityCard classification={classification} />
          <ForecastChart forecastData={forecastPoints} />
        </div>

        {/* Right Side: Map */}
        <div>
          <CycloneMap trackPoints={trackPoints} forecastPoints={forecastPoints} />
        </div>
      </div>
    </div>
  );
}
```

---

## 6. How to Run Frontend & Backend

1. **Terminal 1 (Backend)**:
   ```bash
   python run.py --api-only
   ```
   *(Running at `http://localhost:8000`)*

2. **Terminal 2 (Frontend)**:
   ```bash
   cd frontend
   npm run dev
   ```
   *(Opens at `http://localhost:5173`)*
