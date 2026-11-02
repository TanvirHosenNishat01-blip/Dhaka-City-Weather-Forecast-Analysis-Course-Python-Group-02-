# File: app.py
import os
import csv
import numpy as np
from flask import Flask, render_template, request, send_file
from src.weather_manager import WeatherManager
from src.weather_record import WeatherRecord
from src.analytics import calculate_monthly_metrics, get_diurnal_range
from src.forecaster import compute_rolling_forecast, calculate_errors
from src.health_advisor import assess_heat_stress, assess_respiratory_risk
from src.urban_impact import assess_drainage_stress
from src.event_detector import detect_extreme_events
from src.reporting import export_text_audit, export_json_metrics
from main import find_dataset

app = Flask(__name__)

# Register standard math helpers for Jinja
app.jinja_env.globals.update(min=min, max=max)

# Initialize WeatherManager
manager = WeatherManager()
data_file = find_dataset()
if data_file:
    manager.load_from_csv(data_file)

DHAKA_THANAS = {
    "Mirpur": {"temp_offset": 0.2, "drain_risk": "VERY HIGH", "drain_score": 88, "uhi": "MODERATE", "green_score": 40, "desc_bn": "নিচু এলাকা ও ড্রেনেজ ওভারফ্লোর জন্য পরিচিত; ভারী বর্ষণে কাজীপাড়া ও শেওড়াপাড়ায় জলাবদ্ধতা তৈরি হয়।", "desc_en": "Low-lying basin prone to severe canal overflow and street waterlogging in Kazipara & Shewrapara."},
    "Old Dhaka": {"temp_offset": 1.4, "drain_risk": "HIGH", "drain_score": 82, "uhi": "EXTREME", "green_score": 15, "desc_bn": "ঘনবসতি ও সংকীর্ণ গলির কারণে তীব্র আরবান হিট আইল্যান্ড (+১.৪°C বেশি উষ্ণতা অনুভূত হয়)।", "desc_en": "Extreme Urban Heat Island (+1.4°C thermal offset) due to dense concrete and narrow alleys."},
    "Motijheel": {"temp_offset": 1.2, "drain_risk": "HIGH", "drain_score": 78, "uhi": "HIGH", "green_score": 25, "desc_bn": "বাণিজ্যিক ভবনের তাপ প্রতিফলন ও অফিস ট্রাফিকের কারণে উচ্চ তাপীয় চাপ ও জলাবদ্ধতা ঝুঁকি।", "desc_en": "High commercial thermal mass and severe commuter gridlock during monsoon downpours."},
    "Dhanmondi": {"temp_offset": 0.0, "drain_risk": "MODERATE", "drain_score": 50, "uhi": "MODERATE", "green_score": 72, "desc_bn": "ধানমন্ডি লেক সংলগ্ন বায়ুপ্রবাহ তাপমাত্রা সহনীয় রাখে এবং মাঝারি মানের ড্রেনেজ নেটওয়ার্ক রয়েছে।", "desc_en": "Lake breeze moderates peak daytime heat with moderate urban runoff capacity."},
    "Gulshan": {"temp_offset": -0.6, "drain_risk": "LOW", "drain_score": 30, "uhi": "LOW", "green_score": 85, "desc_bn": "পরিকল্পিত লেক ও বৃক্ষরাজির কারণে তাপমাত্রা মূল শহরের চেয়ে ০.৬°C কম অনুভূত হয়।", "desc_en": "Open green canopy and lake proximity dampen peak temperatures by 0.6°C."},
    "Uttara": {"temp_offset": -0.3, "drain_risk": "MODERATE", "drain_score": 45, "uhi": "MODERATE", "green_score": 78, "desc_bn": "প্রশস্ত সড়ক ও উন্মুক্ত অঞ্চলের কারণে বায়ুপ্রবাহ ভালো এবং পরিকল্পিত নিষ্কাশন ব্যবস্থা রয়েছে।", "desc_en": "Suburban sector layout offering better wind ventilation and moderate drainage stress."},
    "Mohammadpur": {"temp_offset": 0.3, "drain_risk": "HIGH", "drain_score": 75, "uhi": "MODERATE", "green_score": 45, "desc_bn": "বসিলা ও নদী সংলগ্ন নিচু এলাকায় দ্রুত পানি জমে জলাবদ্ধতা সৃষ্টি হওয়ার প্রবণতা রয়েছে।", "desc_en": "Low-lying western periphery prone to rapid water accumulation during monsoon."},
    "Badda/Kuratoli": {"temp_offset": 0.1, "drain_risk": "HIGH", "drain_score": 76, "uhi": "MODERATE", "green_score": 50, "desc_bn": "প্রগতি সরণি ও কুড়াতলী সংলগ্ন এলাকায় ভারী বৃষ্টিতে জলজট ও তীব্র যানজট ঝুঁকি থাকে।", "desc_en": "High risk of street pooling along Pragati Sarani and Kuratoli corridor."}
}

def compute_novel_indices(temp, rh, rain, wind):
    if 25.0 <= temp <= 32.5 and rh >= 72.0:
        dengue_risk = "HIGH BREEDING WINDOW"
        dengue_bn = "উচ্চ ডেঙ্গু প্রজনন ঝুঁকি! (তাপমাত্রা ২৫-৩২°C ও আর্দ্রতা >৭২% এডিস মশার লার্ভা বৃদ্ধির আদর্শ পরিবেশ)। ফুলের টব, ডাবের খোসা ও জমে থাকা পানি পরিষ্কার রাখুন।"
        dengue_en = "High Aedes Breeding Risk! Current temp (25-32°C) & humidity (>72%) create an optimal incubation window. Clear stagnant water immediately."
        dengue_score = 88
    elif 22.0 <= temp <= 35.0 and rh >= 60.0:
        dengue_risk = "MODERATE RISK"
        dengue_bn = "মাঝারি ডেঙ্গু ঝুঁকি। বাসার আশেপাশে স্বচ্ছ পানি জমতে দেবেন না এবং দিনে-রাতে মশারি ব্যবহার করুন।"
        dengue_en = "Moderate vector breeding conditions. Inspect household containers and drains regularly."
        dengue_score = 54
    else:
        dengue_risk = "LOW / UNFAVORABLE"
        dengue_bn = "বর্তমান তাপমাত্রা ও আর্দ্রতা এডিস মশার দ্রুত বংশবৃদ্ধির জন্য কম অনুকূল।"
        dengue_en = "Thermal and moisture levels are currently less favorable for rapid vector incubation."
        dengue_score = 22

    heat_penalty = max(0, (temp - 26.0) * 4.5)
    humidity_penalty = max(0, (rh - 65.0) * 0.6)
    comfort_score = int(max(10, min(100, 100 - heat_penalty - humidity_penalty)))

    cloud_attenuation = min(0.75, (rain * 0.15) + max(0, (rh - 55) / 100.0))
    solar_index = round(5.5 * (1.0 - cloud_attenuation * 0.6), 2)
    cooling_load_pct = int(min(100, max(15, (temp - 20.0) * 5.2 + (rh - 50.0) * 0.4)))

    return {
        "dengue_risk": dengue_risk,
        "dengue_bn": dengue_bn,
        "dengue_en": dengue_en,
        "dengue_score": dengue_score,
        "comfort_score": comfort_score,
        "solar_index": solar_index,
        "cooling_load_pct": cooling_load_pct
    }

def validate_measurements(c_year, c_month, c_day, c_hour, c_temp, c_rh, c_ps, c_ws, c_rain):
    if not (1900 <= c_year <= 2100):
        return False, "ত্রুটি: বছর ১৯০০ থেকে ২১০০ এর মধ্যে হতে হবে!", "Rejected: Year must be between 1900 and 2100."
    if not (1 <= c_month <= 12) or not (1 <= c_day <= 31) or not (0 <= c_hour <= 23):
        return False, "ত্রুটি: মাস (১-১২), দিন (১-৩১) ও ঘণ্টা (০-২৩) সঠিক সীমায় দিন!", "Rejected: Invalid calendar month, day, or hour (0-23)."
    if not (-60.0 <= c_temp <= 60.0):
        return False, "ত্রুটি: তাপমাত্রা (T2M) -60°C থেকে 60°C এর মধ্যে হতে হবে!", "Rejected: Temperature (T2M) must be between -60 and 60 °C."
    if not (0.0 <= c_rh <= 100.0):
        return False, "ত্রুটি: আর্দ্রতা (RH2M) ০% থেকে ১০০% এর মধ্যে হতে হবে! (১০১% গ্রহণযোগ্য নয়)", "Rejected: Relative Humidity (RH2M) must be between 0 and 100%."
    if not (80.0 <= c_ps <= 110.0):
        return False, "ত্রুটি: বায়ুচাপ (PS) ৮০ থেকে ১১০ kPa এর মধ্যে হতে হবে!", "Rejected: Surface Pressure (PS) must be between 80 and 110 kPa."
    if not (0.0 <= c_ws <= 100.0):
        return False, "ত্রুটি: বাতাসের গতিবেগ ০ থেকে ১০০ m/s এর মধ্যে হতে হবে!", "Rejected: Wind speed must be between 0 and 100 m/s."
    if not (0.0 <= c_rain <= 300.0):
        return False, "ত্রুটি: বৃষ্টিপাত ০ থেকে ৩০০ mm/hr এর মধ্যে হতে হবে!", "Rejected: Precipitation must be between 0 and 300 mm/hour."
    return True, "", ""

@app.route("/", methods=["GET", "POST"])
def index():
    selected_year = int(request.values.get("year", 2023))
    selected_month = int(request.values.get("month", 7))
    selected_day = int(request.values.get("day", 15))
    selected_thana = request.values.get("thana", "Mirpur")
    active_tab = request.values.get("active_tab", "v-overview")

    if selected_thana not in DHAKA_THANAS:
        selected_thana = "Mirpur"

    crud_feedback = None
    if request.method == "POST" and request.form.get("action") in ["add_record", "update_record", "delete_record", "save_csv"]:
        action = request.form.get("action")
        active_tab = "v-crud"
        try:
            if action == "save_csv":
                ok, msg = manager.save_working_csv()
                crud_feedback = {
                    "status": "success" if ok else "error",
                    "msg_bn": f"স্থায়ীভাবে সংরক্ষিত হয়েছে: data/weather_records.csv ({len(manager.records)} রেকর্ড)" if ok else msg,
                    "msg_en": msg
                }
            else:
                c_year = int(request.form.get("c_year", selected_year))
                c_month = int(request.form.get("c_month", selected_month))
                c_day = int(request.form.get("c_day", selected_day))
                c_hour = int(request.form.get("c_hour", 0))

                if action == "delete_record":
                    ok, msg = manager.delete_record(c_year, c_month, c_day, c_hour)
                    crud_feedback = {
                        "status": "success" if ok else "error",
                        "msg_bn": f"সফলভাবে {c_year}-{c_month:02d}-{c_day:02d} {c_hour:02d}:00 রেকর্ডটি মুছে ফেলা হয়েছে।" if ok else f"ত্রুটি: {msg}",
                        "msg_en": msg
                    }
                    selected_year, selected_month, selected_day = c_year, c_month, c_day
                else:
                    c_temp = float(request.form.get("c_temp", 25.0))
                    c_rh = float(request.form.get("c_rh", 70.0))
                    c_ps = float(request.form.get("c_ps", 101.0))
                    c_ws = float(request.form.get("c_ws", 2.0))
                    c_rain = float(request.form.get("c_rain", 0.0))

                    valid, err_bn, err_en = validate_measurements(c_year, c_month, c_day, c_hour, c_temp, c_rh, c_ps, c_ws, c_rain)
                    if not valid:
                        crud_feedback = {"status": "error", "msg_bn": err_bn, "msg_en": err_en}
                    elif action == "add_record":
                        new_rec = WeatherRecord(c_year, c_month, c_day, c_hour, c_temp, c_rh, c_ps, c_ws, c_rain)
                        ok, msg = manager.add_custom_record(new_rec)
                        crud_feedback = {
                            "status": "success" if ok else "error",
                            "msg_bn": f"সফলভাবে নতুন রেকর্ড যুক্ত হয়েছে: {new_rec}" if ok else f"ত্রুটি: একই সময়ে একাধিক রেকর্ড গ্রহণযোগ্য নয় ({msg})",
                            "msg_en": f"{msg}: {new_rec}" if ok else msg
                        }
                        if ok:
                            selected_year, selected_month, selected_day = c_year, c_month, c_day
                    elif action == "update_record":
                        ok, msg = manager.update_record(c_year, c_month, c_day, c_hour, c_temp, c_rh, c_ps, c_ws, c_rain)
                        crud_feedback = {
                            "status": "success" if ok else "error",
                            "msg_bn": f"সফলভাবে {c_year}-{c_month:02d}-{c_day:02d} {c_hour:02d}:00 এর রেকর্ড আপডেট হয়েছে!" if ok else f"ত্রুটি: {msg}",
                            "msg_en": msg
                        }
                        if ok:
                            selected_year, selected_month, selected_day = c_year, c_month, c_day
        except ValueError:
            crud_feedback = {"status": "error", "msg_bn": "ত্রুটি: সকল ঘরে সঠিক সংখ্যা (Numeric value) ইনপুট দিন!", "msg_en": "Validation Error: All measurement inputs must be valid numbers."}

    # Fetch base daily observations
    base_records = manager.get_records_by_date(selected_year, selected_month, selected_day)
    if not base_records:
        base_records = manager.records[:24]

    thana_info = DHAKA_THANAS[selected_thana]
    offset = thana_info["temp_offset"]

    # Adjust hourly records for selected Thana + Commute Window Tagging
    thana_hourly = []
    for r in base_records:
        t_adj = round(r.temperature + offset, 2)
        feels = round(-8.784 + 1.611*t_adj + 2.338*(r.humidity/10) - 0.146*t_adj*(r.humidity/10), 2) if t_adj >= 25 else t_adj

        if feels >= 38.0 or r.precipitation >= 8.0 or r.wind_speed >= 10.0:
            commute_status = "AVOID"
            commute_bn = "ঝুঁকিপূর্ণ"
            commute_color = "rose"
        elif feels >= 32.0 or r.precipitation >= 2.0:
            commute_status = "CAUTION"
            commute_bn = "সতর্কতা"
            commute_color = "amber"
        else:
            commute_status = "OPTIMAL"
            commute_bn = "নিরাপদ"
            commute_color = "emerald"

        thana_hourly.append({
            "hour": r.hour,
            "raw_temp": r.temperature,
            "temp": t_adj,
            "humidity": r.humidity,
            "pressure": r.pressure,
            "rain": r.precipitation,
            "wind": r.wind_speed,
            "feels_like": feels,
            "commute_status": commute_status,
            "commute_bn": commute_bn,
            "commute_color": commute_color
        })

    mid_rec = thana_hourly[min(12, len(thana_hourly)-1)]

    # Multi-Thana Comparative Matrix
    base_peak = max(r.temperature for r in base_records)
    base_rh = sum(r.humidity for r in base_records) / len(base_records)
    base_rain_6h = sum(r.precipitation for r in base_records[:6])

    thana_comparison = []
    for t_key, t_meta in DHAKA_THANAS.items():
        t_peak = round(base_peak + t_meta["temp_offset"], 1)
        t_feels = round(-8.784 + 1.611*t_peak + 2.338*(base_rh/10) - 0.146*t_peak*(base_rh/10), 1) if t_peak >= 25 else t_peak
        t_comfort = int(max(10, min(100, 100 - max(0, (t_peak - 26.0)*4.5) - max(0, (base_rh - 65.0)*0.6))))
        flood_depth_cm = round(base_rain_6h * (t_meta["drain_score"] / 18.0), 1)
        thana_comparison.append({
            "name": t_key,
            "uhi": t_meta["uhi"],
            "offset": t_meta["temp_offset"],
            "peak_temp": t_peak,
            "feels_like": t_feels,
            "drain_risk": t_meta["drain_risk"],
            "drain_score": t_meta["drain_score"],
            "green_score": t_meta["green_score"],
            "comfort_score": t_comfort,
            "flood_depth_cm": flood_depth_cm
        })

    # Analytics & Forecasting
    monthly_stats = calculate_monthly_metrics(manager.records, selected_year, selected_month)
    if not monthly_stats:
        monthly_stats = calculate_monthly_metrics(manager.records, 2023, 7)

    dtr = get_diurnal_range(base_records)
    forecast = compute_rolling_forecast(base_records)

    actual_temps = [item["temp"] for item in thana_hourly]
    mean_est = forecast["projected_temperature"] + offset
    predicted_temps = [round(mean_est + (i - 12)*0.05, 2) for i in range(len(actual_temps))]
    eval_metrics = calculate_errors(actual_temps, predicted_temps)

    peak_temp = max(item["temp"] for item in thana_hourly)
    avg_rh = sum(item["humidity"] for item in thana_hourly) / len(thana_hourly)
    total_day_rain = sum(item["rain"] for item in thana_hourly)
    avg_wind = sum(item["wind"] for item in thana_hourly) / len(thana_hourly)

    health = assess_heat_stress(peak_temp, avg_rh)
    drainage = assess_drainage_stress(base_records[:6])
    novel = compute_novel_indices(peak_temp, avg_rh, total_day_rain, avg_wind)

    radar_heat_score = int(min(100, max(0, health["apparent_temp"] * 2.2)))

    if dtr >= 10.0:
        resp_msg_bn = f"দিন ও রাতের তাপমাত্রার পার্থক্য অনেক বেশি ({dtr:.1f}°C > ১০°C)। হাঁপানি, সর্দি-কাশি ও শ্বাসকষ্টের ঝুঁকি বেশি।"
        resp_msg_en = f"Wide day-night temperature swing ({dtr:.1f}°C > 10°C). Elevated risk of asthma, viral flu, and bronchitis."
    else:
        resp_msg_bn = f"দিন ও রাতের তাপমাত্রার পার্থক্য স্বাভাবিক সীমায় রয়েছে ({dtr:.1f}°C)।"
        resp_msg_en = f"Diurnal temperature variation ({dtr:.1f}°C) remains within comfortable daily bounds."

    cond_en = forecast["condition_summary"]
    if "Rain" in cond_en:
        cond_bn = "বৃষ্টিপাতের উচ্চ সম্ভাবনা (অতিরিক্ত আর্দ্রতা ও নিম্নমুখী বায়ুচাপ)"
    elif "Extreme Heat" in cond_en:
        cond_bn = "তীব্র তাপপ্রবাহ সতর্কতা (হিটওয়েভ পরিস্থিতি)"
    elif "Cold" in cond_en:
        cond_bn = "শীতল আবহাওয়া ও কুয়াশাচ্ছন্ন শুষ্ক পরিস্থিতি"
    else:
        cond_bn = "স্থিতিশীল ও সহনীয় আবহাওয়া পরিস্থিতি"

    if thana_info["drain_risk"] in ["VERY HIGH", "HIGH"] and drainage["total_rain_accumulated"] >= 8.0:
        thana_drain_status = "CRITICAL LOCALIZED INUNDATION"
        thana_drain_msg_bn = f"{selected_thana} এলাকায় ৬ ঘণ্টায় {drainage['total_rain_accumulated']} মিমি বৃষ্টির ফলে ড্রেনেজ উপচে রাস্তায় পানি জমে যাওয়ার উচ্চ ঝুঁকি রয়েছে।"
        thana_drain_msg_en = f"Critical inundation risk in {selected_thana} ({drainage['total_rain_accumulated']} mm in 6h). Heavy traffic disruption expected."
    else:
        thana_drain_status = drainage["drainage_status"]
        thana_drain_msg_bn = f"গত ৬ ঘণ্টায় সংগৃহীত বৃষ্টিপাত ({drainage['total_rain_accumulated']} মিমি) {selected_thana} এলাকার ড্রেনেজ ধারণক্ষমতার মধ্যে রয়েছে।"
        thana_drain_msg_en = drainage["traffic_impact"]

    year_records = [r for r in manager.records if r.year == selected_year]
    month_records = [r for r in year_records if r.month == selected_month]
    extremes_year = detect_extreme_events(year_records, temp_thresh=35.0 - offset, rain_thresh=12.0, wind_thresh=10.0)
    extremes_month = detect_extreme_events(month_records, temp_thresh=35.0 - offset, rain_thresh=12.0, wind_thresh=10.0)

    chart_24h_labels = [f"{item['hour']:02d}:00" for item in thana_hourly]
    chart_24h_temps = [item["temp"] for item in thana_hourly]
    chart_24h_feels = [item["feels_like"] for item in thana_hourly]
    chart_24h_rains = [item["rain"] for item in thana_hourly]

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    seasonal_temps = []
    seasonal_rains = []
    for m_idx in range(1, 13):
        m_sub = [r for r in year_records if r.month == m_idx]
        if m_sub:
            seasonal_temps.append(round(float(np.mean([r.temperature + offset for r in m_sub])), 2))
            seasonal_rains.append(round(float(np.sum([r.precipitation for r in m_sub])), 1))
        else:
            seasonal_temps.append(0)
            seasonal_rains.append(0)

    available_years = sorted(list(manager.years_set))
    yearly_labels = [str(y) for y in available_years]
    yearly_avg_temps = []
    yearly_total_rains = []
    for y_val in available_years:
        y_sub = [r for r in manager.records if r.year == y_val]
        if y_sub:
            yearly_avg_temps.append(round(float(np.mean([r.temperature + offset for r in y_sub])), 2))
            yearly_total_rains.append(round(float(np.sum([r.precipitation for r in y_sub])), 1))

    return render_template(
        "index.html",
        total_records=len(manager.records),
        selected_year=selected_year,
        selected_month=selected_month,
        selected_day=selected_day,
        selected_thana=selected_thana,
        active_tab=active_tab,
        thanas=DHAKA_THANAS,
        thana_info=thana_info,
        thana_comparison=thana_comparison,
        available_years=available_years,
        hourly_records=thana_hourly,
        mid_rec=mid_rec,
        monthly_stats=monthly_stats,
        forecast=forecast,
        eval_metrics=eval_metrics,
        cond_bn=cond_bn,
        cond_en=cond_en,
        health=health,
        radar_heat_score=radar_heat_score,
        drainage=drainage,
        thana_drain_status=thana_drain_status,
        thana_drain_msg_bn=thana_drain_msg_bn,
        thana_drain_msg_en=thana_drain_msg_en,
        dtr=round(dtr, 2),
        resp_msg_bn=resp_msg_bn,
        resp_msg_en=resp_msg_en,
        extremes_year=extremes_year,
        extremes_month=extremes_month,
        novel=novel,
        crud_feedback=crud_feedback,
        chart_24h_labels=chart_24h_labels,
        chart_24h_temps=chart_24h_temps,
        chart_24h_feels=chart_24h_feels,
        chart_24h_rains=chart_24h_rains,
        month_names=month_names,
        seasonal_temps=seasonal_temps,
        seasonal_rains=seasonal_rains,
        yearly_labels=yearly_labels,
        yearly_avg_temps=yearly_avg_temps,
        yearly_total_rains=yearly_total_rains
    )

@app.route("/export/<filetype>")
def export_report(filetype):
    year = int(request.args.get("year", 2023))
    month = int(request.args.get("month", 7))
    day = int(request.args.get("day", 15))
    thana = request.args.get("thana", "Mirpur")

    stats = calculate_monthly_metrics(manager.records, year, month)
    if not stats:
        stats = calculate_monthly_metrics(manager.records, 2023, 7)

    sample_records = manager.get_records_by_date(year, month, day)
    if not sample_records:
        sample_records = manager.records[:24]

    fc = compute_rolling_forecast(sample_records)
    peak_t = max(r.temperature for r in sample_records)
    avg_rh = sum(r.humidity for r in sample_records) / len(sample_records)
    health = assess_heat_stress(peak_t, avg_rh)
    drain = assess_drainage_stress(sample_records[:6])

    if filetype == "txt":
        txt_path = f"output/Dhaka_{thana}_{year}_{month:02d}_{day:02d}_Audit.txt"
        export_text_audit(txt_path, stats, fc, health, drain, year, month)
        return send_file(txt_path, as_attachment=True)
    elif filetype == "json":
        json_path = f"output/Dhaka_{thana}_{year}_{month:02d}_Metrics.json"
        export_json_metrics(json_path, stats)
        return send_file(json_path, as_attachment=True)
    elif filetype == "csv":
        csv_path = f"output/Dhaka_{thana}_{year}_{month:02d}_{day:02d}_Records.csv"
        os.makedirs("output", exist_ok=True)
        with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["YEAR", "MO", "DY", "HR", "T2M", "RH2M", "PS", "WS10M", "PRECTOTCORR"])
            writer.writeheader()
            for r in sample_records:
                writer.writerow(r.to_row())
        return send_file(csv_path, as_attachment=True)
    return "Invalid format", 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
