
🌤️ **Dhaka City Weather Forecast & Trend Analysis System**

An end-to-end meteorological analysis and statistical weather forecasting system developed for **CSC 4162: Programming in Python**. The system processes multi-year hourly climate data for Dhaka City (2019–2024) to provide historical trend evaluation, extreme weather alerts, and short-term rolling forecasts.

The implementation strictly demonstrates core Python fundamentals, Object-Oriented Programming (OOP), standard data structures, and mathematical vectorization via NumPy without relying on black-box predictive libraries.

---

📌 **Table of Contents**

* 🎯 Project Overview
* ✨ Key Features
* 📊 Dataset Specifications
* 🏗️ Architecture & OOP Design
* 🧠 Core Python Concepts Used
* 📂 Directory Layout
* ⚙️ Installation & Running
* 💻 Sample Console Walkthrough
* 🛡️ Exception Handling & Robustness

---

🎯 **Project Overview**

Urban microclimates in megacities like Dhaka exhibit sharp seasonal dynamics, characterized by heavy monsoon downpours, localized heat surges, and distinct post-monsoon humidity shifts. This project builds a transparent, high-throughput Python data engine capable of parsing, indexing, and analyzing over 52,000 hourly historical records.

Rather than delegating forecasting to automated machine learning packages, predictive metrics and weather states are computed directly through transparent mathematical models: rolling moving averages, standard deviations, and rule-based threshold filters.

---

✨ **Key Features**

* 🔍 **Temporal Weather Lookup:** Query historical conditions by exact timestamp (Year, Month, Day, Hour) with input validation and instant retrieval via hash-indexed lookups.


* 📈 **Aggregated Statistical Analysis:** Calculate yearly and monthly averages, medians, minimums, maximums, and standard deviations using NumPy.


* ⚠️ **Extreme Event Detection:** Automatically filter and flag high-heat days (>35°C), heavy rainfall events (>10 mm/hr), and rapid barometric pressure drops indicating cyclonic disturbances.


* 🔮 **24-Hour Rolling Forecast:** Estimate next-window temperatures and precipitation likelihood using rolling moving averages and rule-based threshold analysis.
* 💾 **Data Persistence:** Export detailed summary reports and forecast breakdowns directly to clean `.txt` files.



---

📊 **Dataset Specifications**

* 🌐 **Source:** NASA Prediction of Worldwide Energy Resources (POWER) API / MERRA-2 Hourly Resolution


* 📍 **Domain:** Dhaka, Bangladesh (`23.8103° N`, `90.4125° E`, Elevation: ~10.06 m)


* 🗓️ **Timeline:** January 1, 2019, 00:00 LST – December 31, 2024, 23:00 LST


* 🔢 **Total Record Count:** 52,608 hourly entries


* 🌡️ **Parameters Tracked:**
* `T2M`: Temperature at 2 Meters (°C)


* `RH2M`: Relative Humidity at 2 Meters (%)


* `PS`: Surface Pressure (kPa)


* `WS10M`: Wind Speed at 10 Meters (m/s)


* `PRECTOTCORR`: Precipitation / Rainfall (mm/hour)





---

🏗️ **Architecture & OOP Design**

The system implements a decoupled architecture enforcing separation of concerns across data modeling, orchestration, analytics, and user interfaces:

<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/4c6a5876-bc79-446d-ad3f-7d30b67e9aae" />


* 📦 **`WeatherRecord` Class:** Encapsulates an individual hourly observation, maintaining attributes for date components and atmospheric variables with built-in formatters and status helpers.


* 🎛️ **`WeatherManager` Class:** Manages the collection of records, parses CSV data (skipping 14 lines of NASA metadata), enforces uniqueness checks, and handles query dispatching.



---

🧠 **Core Python Concepts Used**

* 🗃️ **Data Structures (FR-3):**
* `list`: Stores all 52,608 sequential `WeatherRecord` objects chronologically.


* `dict`: Hash mapping `(Year, Month, Day) -> [WeatherRecord]` for fast O(1) daily lookups.


* `set`: Tracks unique years, months, and distinct weather alert tags to prevent redundant computations.


* `tuple`: Holds immutable menu options, coordinate bounds, and threshold limits.




* 📐 **NumPy Integration:** Computes multi-year statistical metrics, correlations, and moving average trends efficiently.


* 🔁 **Control Flow & Functions:** Modular functions for data transformations, nested loops for record traversal, and logical branches evaluating atmospheric states.



---

📂 **Directory Layout**

```text
dhaka-weather-forecast-analysis/
│
├── .gitignore
├── requirements.txt
├── README.md
├── main.py
│
├── data/
│   └── dhaka_hourly_weather_2019_2024.csv
│
├── src/
│   ├── __init__.py
│   ├── weather_record.py
│   ├── weather_manager.py
│   ├── analytics.py
│   ├── forecaster.py
│   └── interface.py
│
└── output/
    └── weather_summary_report.txt

```

---

⚙️ **Installation & Running**

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/dhaka-weather-forecast-analysis.git
cd dhaka-weather-forecast-analysis

```


2. Install dependencies:
```bash
pip install -r requirements.txt

```


3. Launch the application:
```bash
python main.py

```



---

💻 **Sample Console Walkthrough**

```text
============================================================
   DHAKA CITY WEATHER ANALYSIS & FORECASTING SYSTEM
   Dataset: 2019-2024 | Total Records: 52,608
============================================================
[1] Search Weather by Specific Date & Hour
[2] View Monthly & Yearly Climate Trends
[3] Scan for Extreme Weather Alerts (Heatwave / Heavy Rain)
[4] Generate 24-Hour Rolling Forecast
[5] Export Statistical Summary Report
[6] Exit
------------------------------------------------------------
Enter your choice (1-6): 2

Enter Target Year (2019-2024): 2023
Enter Target Month (1-12): 7

--- Monthly Summary for Dhaka (July 2023) ---
Total Recorded Hours : 744 hrs
Average Temperature  : 29.42 °C (Min: 24.80 °C, Max: 36.15 °C)
Average Humidity     : 82.14 %
Average Air Pressure : 99.85 kPa
Total Rainfall       : 342.60 mm
Current Status       : Wet / Heavy Monsoon Period
------------------------------------------------------------

```

---

🛡️ **Exception Handling & Robustness**

* 📁 **File Safety:** Verifies dataset path integrity; gracefully catches `FileNotFoundError` or malformed CSV rows without crashing.


* ⌨️ **Input Validation:** Rejects non-numeric menu inputs, invalid calendar dates, and out-of-range hours using robust `try-except` loops.


* 🔄 **Safe Fallbacks:** When querying out-of-scope dates, the system informs the user clearly and routes cleanly back to the main interactive menu.
