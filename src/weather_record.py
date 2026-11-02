# File: src/weather_record.py
# Purpose: OOP Entity Class representing a single hourly weather observation

class WeatherRecord:
    def __init__(self, year, month, day, hour, temp, humidity, pressure, wind_speed, precip):
        # Numeric conversions and variable validation
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hour)
        self.temperature = float(temp)
        self.humidity = float(humidity)
        self.pressure = float(pressure)
        self.wind_speed = float(wind_speed)
        self.precipitation = float(precip)

    def get_date_tuple(self):
        # Immutable Tuple representation for dictionary indexing
        return (self.year, self.month, self.day)

    def calculate_feels_like(self):
        # Simplified Steadman Heat Index formula for apparent temperature
        # Useful for tropical humid climate like Dhaka
        t = self.temperature
        rh = self.humidity
        if t >= 25.0:
            # Heat index approximation
            hi = -8.784 + 1.611*t + 2.338*(rh/10) - 0.146*t*(rh/10)
            return round(hi, 2)
        return round(t, 2)

    def is_rainy(self):
        # Detect rainfall presence in this hourly window
        return self.precipitation > 0.0

    def to_row(self):
        # Convert internal state to a dictionary row matching CSV headers
        return {
            "YEAR": self.year,
            "MO": self.month,
            "DY": self.day,
            "HR": self.hour,
            "T2M": f"{self.temperature:.2f}",
            "RH2M": f"{self.humidity:.2f}",
            "PS": f"{self.pressure:.2f}",
            "WS10M": f"{self.wind_speed:.2f}",
            "PRECTOTCORR": f"{self.precipitation:.2f}"
        }

    def __str__(self):
        # Clean formatted representation of this hourly record
        return (f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:00 | "
                f"Temp: {self.temperature:.1f}°C (Feels: {self.calculate_feels_like():.1f}°C) | "
                f"Humidity: {self.humidity:.1f}% | Rain: {self.precipitation:.2f}mm")
