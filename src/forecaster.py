# File: src/forecaster.py
# Purpose: Statistical moving average forecasting with uncertainty bounds and error evaluation

import numpy as np

def compute_rolling_forecast(recent_24h_records):
    if len(recent_24h_records) < 24:
        return None

    temps = np.array([r.temperature for r in recent_24h_records[-24:]])
    humidities = np.array([r.humidity for r in recent_24h_records[-24:]])
    pressures = np.array([r.pressure for r in recent_24h_records[-24:]])

    # Moving Average estimate
    proj_temp = float(np.mean(temps))
    temp_uncertainty = float(np.std(temps))  # Sigma bound addressing PDF limitation
    avg_humidity = float(np.mean(humidities))
    pressure_trend = float(pressures[-1] - pressures[0])

    if avg_humidity >= 80.0 and pressure_trend < -0.2:
        condition = "High Probability of Rain (High RH + Low Barometric Pressure)"
    elif proj_temp >= 35.0:
        condition = "Extreme Heat Advisory"
    elif proj_temp <= 16.0:
        condition = "Cold Spell / Foggy Dry Weather"
    else:
        condition = "Stable / Moderate Weather"

    return {
        "projected_temperature": proj_temp,
        "uncertainty_sigma": temp_uncertainty,
        "expected_range": (round(proj_temp - temp_uncertainty, 2), round(proj_temp + temp_uncertainty, 2)),
        "mean_humidity": avg_humidity,
        "pressure_trend": pressure_trend,
        "condition_summary": condition
    }

def calculate_errors(actual_vals, predicted_vals):
    # Pure Python MAE and RMSE calculation without black-box ML
    actual = np.array(actual_vals)
    pred = np.array(predicted_vals)
    diff = pred - actual
    
    mae = float(np.mean(np.abs(diff)))
    rmse = float(np.sqrt(np.mean(diff ** 2)))
    
    return {"mae": round(mae, 3), "rmse": round(rmse, 3)}
