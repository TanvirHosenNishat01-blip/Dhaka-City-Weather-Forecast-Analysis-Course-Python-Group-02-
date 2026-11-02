# File: src/urban_impact.py
# Purpose: Monitors urban drainage overload risk and localized flash flood potential


def assess_drainage_stress(consecutive_rain_records):
    # Calculates rolling 3 to 6-hour rainfall accumulation
    total_rain = sum(r.precipitation for r in consecutive_rain_records)
    hours = len(consecutive_rain_records)

    if total_rain >= 35.0:
        status = "CRITICAL / SEVERE WATERLOGGING"
        warning = (
            f"Severe rainfall accumulation ({total_rain:.1f} mm in {hours} hrs). "
            "High probability of urban road inundation in Mirpur, Kazipara, Malibagh, and Shantinagar."
        )
    elif total_rain >= 15.0:
        status = "MODERATE DRAINAGE STRESS"
        warning = (
            f"Noticeable rainfall accumulation ({total_rain:.1f} mm in {hours} hrs). "
            "Commuters may face localized road waterlogging and traffic congestion."
        )
    else:
        status = "NORMAL / LOW RUNOFF"
        warning = f"Cumulative precipitation ({total_rain:.1f} mm in {hours} hrs) is safely within urban drainage capacity."

    return {
        "total_rain_accumulated": round(total_rain, 2),
        "hours_evaluated": hours,
        "drainage_status": status,
        "traffic_impact": warning,
    }
