# File: src/weather_manager.py
# Purpose: Manages weather records, O(1) dictionary lookups, CRUD operations, and CSV persistence

import os
import csv
from src.weather_record import WeatherRecord

class WeatherManager:
    def __init__(self):
        # List: Ordered WeatherRecord objects
        self.records = []
        # Dict: (Year, Month, Day) -> list of hourly WeatherRecord objects
        self.date_index = {}
        # Dict: (Year, Month, Day, Hour) -> exact WeatherRecord object for O(1) CRUD
        self.by_timestamp = {}
        # Set: Unique years available
        self.years_set = set()
        # Tuple: Fixed meteorological parameter identifiers
        self.supported_parameters = ("T2M", "RH2M", "PS", "WS10M", "PRECTOTCORR")
        self.working_csv_path = "data/weather_records.csv"

    def load_from_csv(self, filepath):
        if not os.path.exists(filepath):
            print(f"[ERROR] CSV file not found at: {filepath}")
            return False

        try:
            temp_records = []
            temp_date_index = {}
            temp_by_ts = {}
            temp_years = set()

            with open(filepath, mode='r', encoding='utf-8') as f:
                first_line = f.readline()
                f.seek(0)
                # Detect if NASA POWER 14-line header exists or if it is a clean working CSV
                if "YEAR" not in first_line:
                    for _ in range(14):
                        next(f)

                reader = csv.DictReader(f)
                for row in reader:
                    record = WeatherRecord(
                        year=row['YEAR'],
                        month=row['MO'],
                        day=row['DY'],
                        hour=row['HR'],
                        temp=row['T2M'],
                        humidity=row['RH2M'],
                        pressure=row['PS'],
                        wind_speed=row['WS10M'],
                        precip=row['PRECTOTCORR']
                    )
                    ts_key = (record.year, record.month, record.day, record.hour)
                    if ts_key in temp_by_ts:
                        continue  # Prevent duplicate timestamps

                    temp_records.append(record)
                    temp_by_ts[ts_key] = record
                    temp_years.add(record.year)

                    d_key = record.get_date_tuple()
                    if d_key not in temp_date_index:
                        temp_date_index[d_key] = []
                    temp_date_index[d_key].append(record)

            if not temp_records:
                print("[ERROR] No valid observations found in CSV.")
                return False

            self.records = temp_records
            self.date_index = temp_date_index
            self.by_timestamp = temp_by_ts
            self.years_set = temp_years
            print(f"[SUCCESS] Loaded {len(self.records)} hourly observations into memory.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load data from {filepath}: {e}")
            return False

    def get_records_by_date(self, year, month, day):
        recs = self.date_index.get((int(year), int(month), int(day)), [])
        return sorted(recs, key=lambda r: r.hour)

    def add_custom_record(self, record):
        ts_key = (record.year, record.month, record.day, record.hour)
        if ts_key in self.by_timestamp:
            return False, "Duplicate Timestamp: An observation already exists for this exact hour."

        self.records.append(record)
        self.by_timestamp[ts_key] = record
        self.years_set.add(record.year)
        d_key = record.get_date_tuple()
        if d_key not in self.date_index:
            self.date_index[d_key] = []
        self.date_index[d_key].append(record)
        return True, "Record added successfully."

    def update_record(self, year, month, day, hour, temp, rh, ps, ws, rain):
        ts_key = (int(year), int(month), int(day), int(hour))
        if ts_key not in self.by_timestamp:
            return False, "Record not found for the specified timestamp."

        rec = self.by_timestamp[ts_key]
        rec.temperature = float(temp)
        rec.humidity = float(rh)
        rec.pressure = float(ps)
        rec.wind_speed = float(ws)
        rec.precipitation = float(rain)
        return True, "Record updated successfully."

    def delete_record(self, year, month, day, hour):
        if len(self.records) <= 1:
            return False, "Action Prohibited: Cannot delete the final remaining observation."

        ts_key = (int(year), int(month), int(day), int(hour))
        if ts_key not in self.by_timestamp:
            return False, "Record not found for deletion."

        rec = self.by_timestamp.pop(ts_key)
        self.records.remove(rec)
        d_key = (int(year), int(month), int(day))
        if d_key in self.date_index and rec in self.date_index[d_key]:
            self.date_index[d_key].remove(rec)
        return True, "Record deleted successfully."

    def save_working_csv(self, filepath=None):
        target = filepath or self.working_csv_path
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            fieldnames = ["YEAR", "MO", "DY", "HR", "T2M", "RH2M", "PS", "WS10M", "PRECTOTCORR"]
            with open(target, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in self.records:
                    writer.writerow(r.to_row())
            return True, f"Saved {len(self.records)} records to {target}"
        except Exception as e:
            return False, f"Failed to save working CSV: {e}"
