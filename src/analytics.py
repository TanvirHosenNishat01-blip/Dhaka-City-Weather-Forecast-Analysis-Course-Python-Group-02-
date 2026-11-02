# File: src/analytics.py
# Purpose: High-speed statistical evaluations & multi-parameter correlation matrix using NumPy

import numpy as np

def calculate_monthly_metrics(records, year, month):
    subset = [r for r in records if r.year == int(year) and r.month == int(month)]
    if not subset:
        return None

    temps = np.array([r.temperature for r in subset])
    humidities = np.array([r.humidity for r in subset])
    pressures = np.array([r.pressure for r in subset])
    winds = np.array([r.wind_speed for r in subset])
    rains = np.array([r.precipitation for r in subset])

    # Compute 5x5 Pairwise Correlation Matrix
    matrix_data = np.vstack([temps, humidities, pressures, winds, rains])
    corr_matrix = np.corrcoef(matrix_data)

    return {
        "record_count": len(subset),
        "mean_temp": float(np.mean(temps)),
        "min_temp": float(np.min(temps)),
        "max_temp": float(np.max(temps)),
        "median_temp": float(np.median(temps)),
        "std_temp": float(np.std(temps)),
        "mean_humidity": float(np.mean(humidities)),
        "mean_pressure": float(np.mean(pressures)),
        "mean_wind": float(np.mean(winds)),
        "total_rainfall": float(np.sum(rains)),
        "rainy_hours_count": int(np.sum(rains > 0.0)),
        "temp_humidity_corr": float(corr_matrix[0, 1]),
        "corr_matrix": [
            {"param": "Temp (T2M)", "vals": [round(float(v), 2) for v in corr_matrix[0]]},
            {"param": "Humidity (RH2M)", "vals": [round(float(v), 2) for v in corr_matrix[1]]},
            {"param": "Pressure (PS)", "vals": [round(float(v), 2) for v in corr_matrix[2]]},
            {"param": "Wind (WS10M)", "vals": [round(float(v), 2) for v in corr_matrix[3]]},
            {"param": "Rain (PREC)", "vals": [round(float(v), 2) for v in corr_matrix[4]]}
        ]
    }

def get_diurnal_range(day_records):
    if not day_records:
        return 0.0
    temps = np.array([r.temperature for r in day_records])
    return float(np.max(temps) - np.min(temps))
