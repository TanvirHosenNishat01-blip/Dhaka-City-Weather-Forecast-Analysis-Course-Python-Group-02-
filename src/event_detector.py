# File: src/event_detector.py
# Purpose: Identifies extreme meteorological events like heatwaves, downpours, and squalls

def detect_extreme_events(records, temp_thresh=35.0, rain_thresh=12.0, wind_thresh=10.0):
    heatwave_events = []
    heavy_rain_events = []
    squall_events = []

    for r in records:
        if r.temperature >= temp_thresh:
            heatwave_events.append((r.year, r.month, r.day, r.hour, r.temperature))
        if r.precipitation >= rain_thresh:
            heavy_rain_events.append((r.year, r.month, r.day, r.hour, r.precipitation))
        if r.wind_speed >= wind_thresh:
            squall_events.append((r.year, r.month, r.day, r.hour, r.wind_speed))

    return {
        "heatwaves": heatwave_events,
        "heavy_rains": heavy_rain_events,
        "squalls": squall_events
    }
