# File: src/interface.py
# Purpose: Interactive Command-Line Interface (CLI) with ASCII visualizations

from src.analytics import calculate_monthly_metrics, get_diurnal_range
from src.forecaster import compute_rolling_forecast
from src.health_advisor import assess_heat_stress, assess_respiratory_risk
from src.urban_impact import assess_drainage_stress
from src.event_detector import detect_extreme_events
from src.reporting import export_text_audit, export_json_metrics

def draw_ascii_bar(val, min_val=15.0, max_val=42.0, width=20):
    # Visualizes numerical intensity directly in the terminal
    clamped = max(min_val, min(val, max_val))
    norm = (clamped - min_val) / (max_val - min_val)
    filled = int(norm * width)
    return "█" * filled + "░" * (width - filled)

def run_cli_app(manager):
    while True:
        print("\n" + "="*62)
        print("  DHAKA CITY WEATHER INTELLIGENCE & FORECASTING SYSTEM")
        print("="*62)
        print(" [1] Search Hourly Weather by Exact Date")
        print(" [2] Monthly Trend & NumPy Statistical Evaluation")
        print(" [3] 24-Hour Rolling Forecast with Uncertainty (±σ)")
        print(" [4] Public Health Advisor (Heat Stress & Diurnal Swing)")
        print(" [5] Urban Drainage & Waterlogging Vulnerability Check")
        print(" [6] Screen Historical Extreme Events (Heatwave / Storm)")
        print(" [7] Export Audit Report (TXT & JSON)")
        print(" [8] Exit System")
        print("-"*62)

        choice = input("Select an option (1-8): ").strip()

        if choice == '1':
            try:
                y = int(input("Enter Year (2019-2024): "))
                m = int(input("Enter Month (1-12): "))
                d = int(input("Enter Day (1-31): "))
                results = manager.get_records_by_date(y, m, d)
                if results:
                    print(f"\nObservations for {y}-{m:02d}-{d:02d} ({len(results)} hours):")
                    for r in results[:6]:  # preview first 6 hours
                        bar = draw_ascii_bar(r.temperature)
                        print(f"  {r.hour:02d}:00 | {bar} {r.temperature:4.1f}°C | Feels: {r.calculate_feels_like():4.1f}°C | Rain: {r.precipitation:4.2f}mm")
                    print("  ... [Remaining hourly records loaded safely]")
                else:
                    print("[NOTICE] No observations found for that date.")
            except ValueError:
                print("[ERROR] Please input valid integer numbers.")

        elif choice == '2':
            try:
                y = int(input("Enter Year: "))
                m = int(input("Enter Month (1-12): "))
                stats = calculate_monthly_metrics(manager.records, y, m)
                if stats:
                    print(f"\n--- Monthly Summary for {y}-{m:02d} ---")
                    print(f"Record Count       : {stats['record_count']} hours")
                    print(f"Mean Temperature   : {stats['mean_temp']:.2f} °C")
                    print(f"Min / Max Temp     : {stats['min_temp']:.2f} °C / {stats['max_temp']:.2f} °C")
                    print(f"Standard Deviation : {stats['std_temp']:.2f} °C")
                    print(f"Rainfall Total     : {stats['total_rainfall']:.2f} mm")
                    print(f"Correlation (T, RH): {stats['temp_humidity_corr']:.3f}")
                else:
                    print("[NOTICE] No records for that month.")
            except ValueError:
                print("[ERROR] Invalid numeric format.")

        elif choice == '3':
            sample_records = manager.get_records_by_date(2023, 7, 15)
            fc = compute_rolling_forecast(sample_records)
            if fc:
                print("\n--- 24-Hour Statistical Rolling Forecast ---")
                print(f"Expected Temperature : {fc['projected_temperature']:.2f} °C (±{fc['uncertainty_sigma']:.2f})")
                print(f"Confidence Band (68%): {fc['expected_range'][0]} °C - {fc['expected_range'][1]} °C")
                print(f"Atmospheric Status   : {fc['condition_summary']}")

        elif choice == '4':
            day_records = manager.get_records_by_date(2023, 7, 15)
            if day_records:
                peak_temp = max(r.temperature for r in day_records)
                avg_rh = sum(r.humidity for r in day_records) / len(day_records)
                dtr = get_diurnal_range(day_records)

                health = assess_heat_stress(peak_temp, avg_rh)
                resp = assess_respiratory_risk(dtr)

                print("\n--- Biometeorological Health Assessment ---")
                print(f"Peak Air Temp : {peak_temp:.1f}°C | Feels Like: {health['apparent_temp']}°C")
                print(f"Risk Rating   : {health['risk_level']}")
                for tip in health['advisory']:
                    print(f"  * {tip}")
                print(f"\nDiurnal Fluctuation: {dtr:.1f}°C -> {resp['message']}")

        elif choice == '5':
            rainy_subset = manager.get_records_by_date(2023, 7, 15)
            stress = assess_drainage_stress(rainy_subset[:6])
            print("\n--- Urban Drainage & Waterlogging Assessment ---")
            print(f"Rainfall (6-hr Window) : {stress['total_rain_accumulated']} mm")
            print(f"Drainage System Status : {stress['drainage_status']}")
            print(f"Advisory Notice        : {stress['traffic_impact']}")

        elif choice == '6':
            print("\nScanning first 5,000 historical observations...")
            ev = detect_extreme_events(manager.records[:5000])
            print(f"Extreme Heatwaves Recorded : {len(ev['heatwaves'])}")
            print(f"Heavy Downpour Events       : {len(ev['heavy_rains'])}")
            print(f"High Wind Squalls           : {len(ev['squalls'])}")

        elif choice == '7':
            stats = calculate_monthly_metrics(manager.records, 2023, 7)
            fc = compute_rolling_forecast(manager.get_records_by_date(2023, 7, 15))
            health = assess_heat_stress(35.2, 78.0)
            drain = assess_drainage_stress(manager.get_records_by_date(2023, 7, 15)[:6])
            
            txt_path = "output/Dhaka_Weather_Audit_Report.txt"
            json_path = "output/Dhaka_Weather_Metrics.json"
            
            export_text_audit(txt_path, stats, fc, health, drain, 2023, 7)
            export_json_metrics(json_path, stats)

        elif choice == '8':
            print("\nThank you for using Dhaka Weather Forecast Analysis System. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Select 1 to 8.")
