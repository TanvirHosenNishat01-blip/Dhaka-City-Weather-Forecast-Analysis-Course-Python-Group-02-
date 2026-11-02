# File: src/reporting.py
# Purpose: Handles persistent storage and multi-format exports (TXT, JSON, CSV)

import os
import json
import csv

def export_text_audit(filepath, monthly_stats, forecast, health_info, drainage_info, year, month):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("====================================================================\n")
            f.write(f"     DHAKA WEATHER FORECAST & PUBLIC HEALTH AUDIT REPORT\n")
            f.write(f"     Target Period: {year}-{month:02d} | Location: Dhaka, Bangladesh\n")
            f.write("====================================================================\n\n")

            f.write("[1] NUMERICAL METRICS SUMMARY (Pure NumPy):\n")
            f.write(f"  * Total Hours Evaluated   : {monthly_stats['record_count']}\n")
            f.write(f"  * Average Temperature      : {monthly_stats['mean_temp']:.2f} °C\n")
            f.write(f"  * Min / Max Temperature    : {monthly_stats['min_temp']:.2f} °C / {monthly_stats['max_temp']:.2f} °C\n")
            f.write(f"  * Standard Deviation       : {monthly_stats['std_temp']:.2f} °C\n")
            f.write(f"  * Total Rainfall Recorded  : {monthly_stats['total_rainfall']:.2f} mm ({monthly_stats['rainy_hours_count']} rainy hours)\n")
            f.write(f"  * Temp-Humidity Correlation: {monthly_stats['temp_humidity_corr']:.3f}\n\n")

            if forecast:
                f.write("[2] 24-HOUR ROLLING FORECAST & UNCERTAINTY:\n")
                f.write(f"  * Projected Mean Temp      : {forecast['projected_temperature']:.2f} °C (±{forecast['uncertainty_sigma']:.2f})\n")
                f.write(f"  * Confidence Range (68%)   : {forecast['expected_range'][0]} °C - {forecast['expected_range'][1]} °C\n")
                f.write(f"  * Meteorological Condition : {forecast['condition_summary']}\n\n")

            if health_info:
                f.write("[3] PUBLIC HEALTH & HEAT INDEX ASSESSMENT:\n")
                f.write(f"  * Feels-Like Temperature   : {health_info['apparent_temp']} °C\n")
                f.write(f"  * Physiological Risk Level : {health_info['risk_level']}\n")
                f.write("  * Safety Advisory Guidelines:\n")
                for adv in health_info['advisory']:
                    f.write(f"     - {adv}\n")
                f.write("\n")

            if drainage_info:
                f.write("[4] URBAN DRAINAGE & COMMUTER IMPACT:\n")
                f.write(f"  * Status                   : {drainage_info['drainage_status']}\n")
                f.write(f"  * Impact Assessment        : {drainage_info['traffic_impact']}\n")
                f.write("====================================================================\n")
        print(f"[SUCCESS] Audit report written to: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")
        return False

def export_json_metrics(filepath, data_dict):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=4)
        print(f"[SUCCESS] JSON metrics saved to: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] JSON export failed: {e}")
        return False
