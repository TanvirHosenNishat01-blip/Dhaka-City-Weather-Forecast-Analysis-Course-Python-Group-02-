# File: main.py
# Purpose: System entry point; handles initialization, dataset loading, and CLI launch

import os
import sys
from src.weather_manager import WeatherManager
from src.interface import run_cli_app

def find_dataset():
    # Candidates for local and kaggle environments
    candidate_paths = [
        "data/nasa_power_dhaka_weather_timeseries_dataset_2019_to_2024.csv",
        "data/dhaka_hourly_weather_2019_2024.csv",
        "data/weather_records.csv"
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            return p
    return None

def main():
    print("==========================================================")
    print("Initializing Dhaka City Weather Forecasting System...")
    print("American International University-Bangladesh (AIUB)")
    print("==========================================================")

    data_file = find_dataset()
    if not data_file:
        print("[ERROR] Weather dataset CSV not found in data/ folder!")
        print("Please place the CSV file inside the 'data/' directory.")
        sys.exit(1)

    manager = WeatherManager()
    success = manager.load_from_csv(data_file)

    if not success:
        print("[FATAL] Could not initialize weather records. Exiting.")
        sys.exit(1)

    # Launch interactive menu loop
    run_cli_app(manager)

if __name__ == "__main__":
    main()
