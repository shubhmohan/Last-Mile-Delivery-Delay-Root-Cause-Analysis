<div align="center">

<!-- ANIMATED BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F2040,50:0D9488,100:F59E0B&height=200&section=header&text=India%20Last-Mile%20Delivery%20RCA&fontSize=36&fontColor=ffffff&fontAlignY=38&desc=Root%20Cause%20Analysis%20Dashboard&descSize=16&descAlignY=58&animation=fadeIn" width="100%"/>

# 🚚 India Last-Mile Delivery — Root Cause Analysis

**Built by [Shubh Mohan](https://github.com/shubhmohan)**

[![Python](https://img.shields.io/badge/Python-3.11-3B82F6?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![SciPy](https://img.shields.io/badge/SciPy-Statistics-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org)
[![License](https://img.shields.io/badge/License-MIT-16A34A?style=for-the-badge)](LICENSE)

<br>

| 📦 Market Size | 📈 CAGR | 🗂 Dataset | 🎯 Root Causes | 🏙 Cities |
|:---:|:---:|:---:|:---:|:---:|
| **$6.5B** | **13.7%** | **45,593 rows** | **4 Buckets** | **3 Tiers** |

</div>

---

## 📌 Project Overview

A **full-stack data analytics solution** that performs Root Cause Analysis (RCA) on last-mile delivery delays across India. This project goes from raw delivery data to a **production-grade Streamlit dashboard** with live filters, statistical proofs, and a What-If business simulator.

> 💡 **India Context:** India's last-mile market hits $24B by 2033. 30–40% of vehicle route-time is lost to idling in Mumbai and Bengaluru. This project mirrors real problems solved by Delhivery, Shadowfax, Ekart, and Zomato.

---

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| **Language** | Python 3.14 |
| **Data Wrangling** | Pandas, NumPy |
| **Statistics** | SciPy (T-Tests, Z-Score, Pearson r) |
| **Visualisation** | Seaborn, Matplotlib, Plotly |
| **Geospatial** | Folium, Haversine distance |
| **Dashboard** | Streamlit, streamlit-folium |
| **ML / Encoding** | Scikit-learn (get_dummies, correlation) |
| **Export** | openpyxl, PNG (dpi=150) |
| **Notebook** | Jupyter Lab |

---

## 😋 Check Out Now 
India Last Mile Delivery-Root Cause Analysis Dashboard : https://delay-rac.streamlit.app

---

## 📊 Analytical Pipeline

```
Raw CSV (45,593 rows)
    │
    ▼
🔧 PREPROCESSING
    ├── Haversine distance from lat/lon
    ├── Strip dirty text columns ("conditions Cloudy" → "Cloudy")
    ├── Fix Time_taken(min) → "(min)24" → 24 int
    ├── Engineer: Distance_KM, Minutes_Per_KM, On_Time, Success_Rate
    └── Save → data/processed/deliveries_clean.csv
    │
    ▼
📊 PHASE A — DESCRIPTIVE ANALYSIS
    ├── A1: Violin plots → Delay by City type
    ├── A2: Heatmap → Hour of Day × Day of Week
    ├── A3: Boxplot → Delay by Weather condition
    └── A4: Barplot → Avg time by Traffic level
    │
    ▼
🔬 PHASE B — DIAGNOSTIC ANALYSIS
    ├── B1: T-Test → Does weather significantly increase delay? (p < 0.05)
    ├── B2: Z-Score → Flag outlier couriers (Z > 3)
    └── B3: Correlation Matrix → What really drives delay?
    │
    ▼
🎯 ROOT CAUSE BUCKETS (4 categories)
    │
    ▼
🖥️ STREAMLIT MANAGER DASHBOARD
```

---

## 🎯 The 4 RCA Buckets

| # | Bucket | Key India Finding | Statistical Proof | Fix |
|---|---|---|---|---|
| 01 | 🌧 **Environmental** | Fog/Cloudy adds +7 min. Jam traffic adds +10 min. Festival=Yes adds +4 min | T=51.78, **p=0.00000** | Dynamic Promised Time + IMD API |
| 02 | 🏭 **Operational** | `multiple_deliveries` is #1 driver. 3 orders = 47.8 min vs 22.9 min for 0 | **r = 0.38** (strongest) | Smarter order batching at dispatch |
| 03 | 👤 **Behavioural** | 8 outlier couriers (Z>3). Higher ratings → faster delivery (r=-0.32) | **Z > 3**, r = −0.32 | Gamification + retraining program |
| 04 | 🏗 **Structural** | Semi-Urban +22.4 min vs Metro. Mathematically impossible ETAs detected | r = 0.29, violin spread | Retrain ETA model + landmark field |

---

## 🖥️ Dashboard Features

```
┌─────────────────────────────────────────────────────────────┐
│  🚚 India Last-Mile Delivery — RCA Dashboard                │
├─────────┬──────────┬──────────────┬───────────┬────────────┤
│ 26.3min │  52.7%   │   45,593     │  8.5 km   │   4.64     │
│Avg Time │ On-Time  │  Deliveries  │ Avg Dist  │   Rating   │
├─────────┴──────────┴──────────────┴───────────┴────────────┤
│ [City ▼] [Traffic ▼] [Weather ▼] [Festival ○All ○Yes ○No] │
├──────────────────────────┬──────────────────────────────────┤
│ 🚦 Traffic Barplot       │ 🌦 Weather Barplot               │
│ Low→Jam progressive bars │ Sorted by avg delay, fleet line  │
├──────────────────────────┼──────────────────────────────────┤
│ 🏙 City Violin Plot      │ 📦 Multiple Deliveries Chart     │
│ Metro/Urban/Semi-Urban   │ Shows #1 delay driver visually   │
├──────────────────────────┼──────────────────────────────────┤
│ 👤 Z-Score Histogram     │ ⭐ Rating Scatter + Trend Line   │
│ Fleet distribution + 8   │ Proves gamification works        │
│ outlier flags            │ (negative trend r=-0.32)         │
├──────────────────────────┴──────────────────────────────────┤
│ 🎯 RCA Bucket Summary — 4 live cards with real numbers      │
├─────────────────────────────────────────────────────────────┤
│ 🎛️ What-If Simulator                                        │
│   Reduce courier load ──────●────── 2 orders               │
│   Routing AI improvement ───●────── 5 min                  │
│   Rating improvement ───────●────── 0.4 stars              │
│   Current: 52.7%  →  Projected: 75.3%  (+22.6%) ✅         │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/shubhmohan/india-delivery-rca.git
cd india-delivery-rca

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download dataset
# kaggle.com/datasets/gauravmalik26/food-delivery-dataset
# Save to: data/raw/food_delivery_train.csv

# 4. Run preprocessing
jupyter notebook notebooks/01_preprocessing.ipynb

# 5. Launch dashboard
streamlit run dashboard/app.py
```

---

## 📁 Project Structure

```
delivery_rca/
├── data/
│   ├── raw/                    ← Original Kaggle CSV
│   └── processed/              ← Cleaned & feature-engineered
├── notebooks/
│   ├── 01_preprocessing.ipynb  ← Data cleaning + feature engineering
│   ├── 02_phase_a.ipynb        ← Descriptive analysis (4 charts)
│   └── 03_phase_b.ipynb        ← Diagnostic analysis (T-Test, Z-Score)
├── dashboard/
│   └── app.py                  ← Streamlit dashboard (main file)
├── outputs/
│   ├── A1_delay_by_city.png
│   ├── A2_heatmap_hour_vs_day.png
│   ├── A3_delay_by_weather.png
│   ├── A4_delay_by_traffic.png
│   ├── B2_zscore_couriers.png
│   └── B3_correlation.png
├── requirements.txt
└── README.md
```

---

## 🔑 Key Findings

```python
# T-Test: Weather significantly increases delivery time
T-Statistic : 51.781  |  P-Value : 1.24e-580  →  ✅ SIGNIFICANT

# Z-Score: Fleet health
Total couriers  : 1,320
Outlier (Z > 3) : 8 couriers  →  ⚠ Need retraining
Top performers  : 174 couriers →  ⭐ Benchmark these

# Correlation: #1 delay drivers (ranked)
multiple_deliveries     : r = +0.38  ← STRONGEST
Road_traffic_density_Jam: r = +0.35
Festival_Yes            : r = +0.29
Delivery_person_Ratings : r = −0.32  ← Gamification works

# What-If Result (from dashboard)
Current On-Time Rate    : 52.7%
After optimisation      : 75.3%  (+22.6%)
```

---

## 📦 Requirements

```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0
seaborn>=0.12.0
matplotlib>=3.7.0
streamlit>=1.28.0
folium>=0.14.0
streamlit-folium>=0.15.0
scikit-learn>=1.3.0
plotly>=5.17.0
openpyxl>=3.1.0
jupyter>=1.0.0
```

---

## 🗓 Changelog

### ✅ v1.0.0 — March 2025 — Initial Release
- Data cleaning, Haversine distance computation, full feature engineering
- Phase A: 4 descriptive charts (violin, heatmap, boxplot, barplot)
- Phase B: T-Test (p=0.00000), Z-Score outlier detection, correlation matrix
- Streamlit dashboard: 5 KPI cards, 6 charts, RCA bucket summary, What-If simulator

### 🔄 v1.1.0 — Planned Q2 2025 — Maps & Live Weather
- [ ] Folium Red Zone map with city-level delay circles
- [ ] IMD Weather API integration for live monsoon overlay
- [ ] Pin-code level granularity on delivery map
- [ ] Festival calendar auto-detection (Diwali, Eid, Holi)

### 🔄 v1.2.0 — Planned Q3 2025 — ML Prediction Layer
- [ ] Random Forest regressor for ETA prediction
- [ ] SHAP values for explainable AI — feature attribution per delay
- [ ] Model performance dashboard: MAE, RMSE, R² score cards
- [ ] Live prediction input in dashboard → ETA + delay risk score

### 🔮 v2.0.0 — Future Q4 2025 — Live Operations Mode
- [ ] Real-time Delhivery / Shadowfax API connection
- [ ] Real-time anomaly detection for live orders
- [ ] WhatsApp/Slack alerts for Z>3 courier triggers
- [ ] Automated weekly PDF report for ops managers
- [ ] Multi-tenant dashboards per city/hub

### 🔮 v2.1.0 — Future 2026 — NLP Address Intelligence
- [ ] NLP model for Indian address parsing and standardisation
- [ ] Auto-detect missing landmark fields at order creation
- [ ] Pin code validation and auto-correction pipeline
- [ ] Address quality score per delivery zone

---

## 🎤 Interview Answer (STAR Format)

> **Situation:** India's last-mile delivery sector is $6.5B, growing at 13.7% CAGR — but 53% of shipping cost is last-mile alone. Delays directly hurt profitability.
>
> **Task:** Build an end-to-end RCA pipeline to identify *why* deliveries are late across 5 Indian cities, and turn that into a manager-facing dashboard.
>
> **Action:** Used T-Tests to prove monsoon weather statistically increases delays (p=0.00000). Used Z-Scores to flag 8 outlier couriers. Correlation matrix proved `multiple_deliveries` (r=0.38) beats even Jam traffic — changing the recommendation from "hire more riders" to "fix order batching."
>
> **Result:** The What-If simulator shows that reducing courier load + improving routing + training program raises on-time rate from 52.7% → 75.3% (+22.6%). That's a decision-support tool backed by statistical evidence from 45,000 real deliveries.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:F59E0B,50:0D9488,100:0F2040&height=120&section=footer" width="100%"/>

**Made with 🧠 and 📊 by [Shubh Mohan](https://github.com/shubhmohan)**

*India needs more data analysts who understand its logistics challenges.*

</div>
