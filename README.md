# Dhaka City Weather Intelligence, Scientific Diagram & Decision System

A high-performance, modular Python and Flask-based meteorological decision-support system built upon NASA POWER hourly historical observations (2019–2024) for Dhaka City. The application provides exploratory record management, pure NumPy statistical modeling, rolling moving-average projections, localized microclimate adjustments across 8 Dhaka thanas, real-time "What-If" climate simulations, biometeorological health advisories, urban drainage assessments, and advanced scientific diagrams.

Developed for academic coursework (**CSC 4162: Programming in Python**, American International University-Bangladesh - AIUB).

---

## Key Features

### 1. Core Data Architecture & Validated Persistence (F-1 to F-4, F-7)
- **Object-Oriented Record Model (`WeatherRecord`):** Encapsulates hourly measurements (T2M, RH2M, PS, WS10M, PRECTOTCORR) with immutable property validation.
- **Fast Record Coordinate Engine (`WeatherManager`):** Utilizes O(1) dictionary timestamp mapping and set-based duplicate detection.
- **Full In-Memory CRUD Lab:** Add new observations (`F-1`), search/browse paged records (`F-2`), inline-edit measurements (`F-3`), and delete records (`F-4`) with final-record deletion prevention guards.
- **Durable Working CSV Sync (`F-7`):** Seamless synchronization between runtime modifications and `data/weather_records.csv` without modifying the raw NASA POWER source file.

### 2. Numerical Modeling & Forecast Evaluation (F-5, F-6)
- **Pure NumPy Statistical Matrix:** Evaluates mean, standard deviation (std), min/max, median, total rainfall, rainy hours, and correlation coefficients over 52,608 hourly historical records.
- **Rolling Moving-Average Forecaster:** Generates 1-to-24 hour rolling projections (h-hour lookback) accompanied by standard error bands (±1σ).
- **Historical Backtesting & Error Metrics:** Computes Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) against historical test slices.

### 3. Dhaka Microclimate & 8-Thana Comparative Matrix
- **Urban Heat Island (UHI) Offsets:** Tailored canopy and density thermal differentials across 8 strategic Dhaka thanas:
  - **Old Dhaka:** +1.4°C (Extreme UHI, dense concrete alleys)
  - **Motijheel:** +1.2°C (Commercial thermal mass & peak commuter congestion)
  - **Mohammadpur / Mirpur:** +0.2°C to +0.3°C (Basin topography, canal overflow risks)
  - **Badda / Kuratoli:** +0.1°C (Pragati Sarani runoff pooling corridor)
  - **Dhanmondi:** 0.0°C (Baseline lake moderation)
  - **Uttara / Gulshan:** -0.3°C to -0.6°C (Open canopy & suburban wind ventilation)
- **Multi-Thana Radar Profile:** Interactive 5-axis comparative radar diagram evaluating heat stress, drainage vulnerability, vector risk, green canopy, and outdoor workability.

### 4. Interactive "What-If" Climate & Flood Simulator
- Real-time client-side parameter adjustments via reactive sliders without page reloads:
  - **Air Temperature:** 10.0°C to 48.0°C
  - **Relative Humidity:** 20% to 100%
  - **6-Hour Cumulative Rainfall:** 0 mm to 180 mm
  - **Surface Wind Speed:** 0 m/s to 25 m/s
- Instantaneous recalculation of Steadman Heat Index, street waterlogging depth (cm), outdoor productivity scores, photovoltaic solar output estimates (kWh/kWp), vector incubation risk, and cooling electrical grid surge.

### 5. Scientific Diagram Laboratory
- **5x5 Pearson Correlation Heatmap:** Matrix calculating linear dependency between Temperature, Humidity, Pressure, Wind Speed, and Precipitation via vectorized `np.corrcoef()`.
- **Dynamic Physiological Heat Stress Gauge:** Canvas-rendered arc gauge illustrating safety boundaries (Safe, Caution, Danger, Heat Stroke Risk).
- **Aerodynamic Wind Polar Vector Compass:** 24-hour directional velocity and kinetic aerodynamic distribution diagram.
- **24-Hour Diurnal Thermal Curves:** Dual-axis visualization contrasting measured dry-bulb temperature against the apparent heat index curve.
- **Multi-Year Climate Anomaly Engine (2019–2024):** Visual comparative trends of annual mean temperatures and precipitation totals.

### 6. Citizen Public Health & Urban Advisory
- **Dengue Vector Breeding Environmental Risk Index:** Bio-meteorological risk detection modeling optimal Aedes mosquito incubation windows (25.0°C to 32.5°C and RH ≥ 72%).
- **Diurnal Temperature Range (DTR) Respiratory Warnings:** Automated detection of wide day-night swings (DTR ≥ 10.0°C) signaling elevated risks for asthma, bronchitis, and viral flu.
- **Urban Drainage & Street Pooling Monitor:** Evaluates 6-hour rainfall accumulation against localized thana drainage capacities to issue commuter congestion warnings.
- **Smart 24-Hour Commute Planner Strip:** Color-coded hourly flags (Optimal, Caution, Avoid) for students and transit commuters.

### 7. Dual-Language & Multi-Format Reporting
- **Bilingual Interface:** Toggle between English and Bengali (**বাংলা**) across all views, preserving UI state across requests.
- **Multi-Format Exports:** Export filtered observations and analytical summaries to text audits (`.txt`), structured metrics (`.json`), or filtered comma-separated values (`.csv`).
- **Academic Print Engine:** Dedicated print stylesheet formatting the complete diagnostic suite into an audit-ready laboratory report.

---

## Project Structure

```text
├── assets/                  # Static design assets and system diagrams
├── data/                    # Historical and active datasets
│   ├── nasa_power_dhaka_weather_timeseries_dataset_2019_to_2024.csv
│   └── weather_records.csv  # Working persistent CSV file
├── output/                  # Generated audit reports (.txt, .json, .csv)
├── src/                     # Modular Python logic
│   ├── init.py
│   ├── analytics.py         # NumPy metrics and Pearson correlation matrix
│   ├── event_detector.py    # Extreme weather events screening
│   ├── forecaster.py        # Rolling moving-average and MAE/RMSE calculations
│   ├── health_advisor.py    # Biometeorological stress and respiratory rules
│   ├── interface.py         # Console-based interactive CLI application
│   ├── reporting.py         # Multi-format report export handlers
│   ├── urban_impact.py      # Urban drainage stress and waterlogging formulas
│   ├── weather_manager.py   # Record coordinator, indexes, and CRUD persistence
│   └── weather_record.py    # WeatherRecord domain entity and validation logic
├── templates/
│   └── index.html           # Single Page Application UI with Chart.js diagrams
├── .gitignore               # Ignores virtual environments, caches, and outputs
├── app.py                   # Flask Web Dashboard entry point
├── main.py                  # CLI / Application bootstrap entry point
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/TanvirHosenNishat01-blip/Dhaka-City-Weather-Forecast-Analysis-Course-Python-Group-02-.git
cd Dhaka-City-Weather-Forecast-Analysis-Course-Python-Group-02-
```

### 2. Configure Virtual Environment
On Windows (Git Bash):
```bash
python -m venv venv
source venv/Scripts/activate
```

On Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

### Option A: Interactive Web Dashboard (Recommended)
Launch the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Option B: Terminal-Based CLI Interface
To run the interactive menu-driven command-line application:
```bash
python main.py
```

---

## Input Validation Rules

The application implements defensive data validation guards:
- **Timestamp:** Calendar timestamps strictly formatted as `YYYY-MM-DD HH:00` within years `1900–2100`.
- **Temperature (T2M):** -60.0°C to +60.0°C.
- **Relative Humidity (RH2M):** 0.0% to 100.0% (values like 101% are rejected).
- **Surface Pressure (PS):** 80.0 kPa to 110.0 kPa.
- **Wind Speed (WS10M):** 0.0 m/s to 100.0 m/s.
- **Precipitation (PRECTOTCORR):** 0.0 mm/hr to 300.0 mm/hr.
- **Uniqueness Guard:** Timestamps must be uniquely indexed; duplicates are rejected during import and manual insertion.
- **Deletion Safeguard:** Removing the final remaining record in the repository is prohibited.

---

## Academic Information

- **Institution:** American International University-Bangladesh (AIUB)
- **Faculty:** Faculty of Science & Technology (FST)
- **Department:** Department of Computer Science
- **Course:** Programming in Python (CSC 4162)
- **Group:** 02 | **Section:** D

### Contributors
1. **Tanvir Hosen Nishat** (ID: 23-51941-2)<br>
2. **Md Al Amin** (ID: 23-52648-2)<br>
3. **Muhammad Tanzimul Islam** (ID: 23-55693-3)
4. **Khan Sajid Ahmed** (ID: 23-51685-2)
5. **Ashfaq Nur** (ID: 23-51714-2)

---

## Disclaimer
This software is developed strictly for educational, analytical, and exploratory data management purposes using non-sensitive environmental data attributed to NASA POWER. It is not an operational municipal emergency warning system or an official real-time meteorological forecasting service.
