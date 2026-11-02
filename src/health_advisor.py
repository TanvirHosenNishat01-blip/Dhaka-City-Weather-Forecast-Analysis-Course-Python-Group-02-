# File: src/health_advisor.py
# Purpose: Health advisory and physiological comfort analysis for Dhaka residents

def assess_heat_stress(temp, humidity):
    # Evaluates physiological stress based on Steadman's Heat Stress Index
    if temp >= 25.0:
        heat_index = -8.784 + 1.611*temp + 2.338*(humidity/10) - 0.146*temp*(humidity/10)
    else:
        heat_index = temp

    if heat_index >= 41.0:
        risk_level = "DANGER / HEAT STROKE RISK"
        advisory = [
            "Avoid direct outdoor sun exposure between 11:30 AM and 3:30 PM.",
            "Mandatory hydration: Drink at least 3.5 to 4 Liters of saline or water.",
            "High vulnerability for elderly, children, and outdoor manual laborers."
        ]
    elif heat_index >= 32.0:
        risk_level = "EXTREME CAUTION / HEAT EXHAUSTION"
        advisory = [
            "Continuous physical activity can trigger fatigue and muscle cramps.",
            "Wear light, loose-fitting cotton clothing and carry an umbrella.",
            "Drink plenty of water before feeling thirsty."
        ]
    elif heat_index >= 27.0:
        risk_level = "CAUTION / MILD FATIGUE"
        advisory = [
            "Comfortable for indoor tasks; prolonged outdoor exercise may cause fatigue.",
            "Maintain standard hydration."
        ]
    else:
        risk_level = "NORMAL / LOW RISK"
        advisory = ["Thermal conditions are comfortable and safe for outdoor activities."]

    return {
        "apparent_temp": round(heat_index, 1),
        "risk_level": risk_level,
        "advisory": advisory
    }

def assess_respiratory_risk(diurnal_range):
    # High diurnal fluctuation (>10°C) triggers respiratory sensitivities in winter
    if diurnal_range >= 10.0:
        return {
            "risk": "ELEVATED RESPIRATORY SENSITIVITY",
            "message": "Wide day-night temperature swing (>10°C). Increased risk of asthma, viral flu, and bronchitis."
        }
    return {
        "risk": "NORMAL",
        "message": "Temperature variation remains within standard daily bounds."
    }
