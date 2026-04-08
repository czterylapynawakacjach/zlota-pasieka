import requests
import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# --- Configuration ---
STATION_NAME = "warszawa"
BASE_TEMP = 10.0
TELEMETRY_FILE = "src/data/telemetry.json"
ARCHIVE_FILE = "src/data/archive.json"
MAX_TELEMETRY = 240  # 30 days of samples
MAX_ARCHIVE = 730    # 2 years of daily data
POLAND_TZ = ZoneInfo("Europe/Warsaw")

def fetch_imgw_data():
    """Pure I/O: Fetches raw data from the IMGW API."""
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{STATION_NAME}"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def calculate_intensity(temp, wind, rain):
    """Calculates Foraging Intensity Index (0-100%)."""
    score = 100 - (wind * 4)
    score = max(0, min(100, score))
    if rain > 0 or temp < 10:
        return 0
    if temp < 14:
        score *= 0.5
    return round(score, 1)

def update_stores():
    """Processing Layer: Handles business logic, rolling windows, and archiving."""
    raw_data = fetch_imgw_data()
    if not raw_data:
        return

    # 1. Standardize Inputs & Logic
    # Use API measurement time if available, otherwise round system time to the hour
    try:
        # API returns data_pomiaru (YYYY-MM-DD) and godzina_pomiaru (HH)
        obs_date = raw_data.get('data_pomiaru')
        obs_hour = int(raw_data.get('godzina_pomiaru'))
        # Create a naive datetime matching the observation time
        timestamp_dt = datetime.strptime(f"{obs_date} {obs_hour}:00", "%Y-%m-%d %H:%M")
    except Exception as e:
        print(f"Warning: Could not parse API time ({e}). Falling back to rounded system time.")
        now_pl = datetime.now(POLAND_TZ).replace(tzinfo=None)
        timestamp_dt = now_pl.replace(minute=0, second=0, microsecond=0)

    t_now = float(raw_data['temperatura'])
    wind_kmh = round(float(raw_data['predkosc_wiatru']) * 3.6, 1)
    rain_mm = float(raw_data['suma_opadu'] or 0)
    pressure = float(raw_data['cisnienie'] or 0)
    humidity = float(raw_data['wilgotnosc_wzgledna'] or 0)
    
    # 3-Tier Status Logic
    if rain_mm > 0 or t_now < 10:
        status = "Restricted"
    elif t_now > 14 and wind_kmh < 20:
        status = "Optimal"
    else:
        status = "Marginal"

    delta_t = round(t_now * (1 - (humidity / 100)), 1)
    intensity = calculate_intensity(t_now, wind_kmh, rain_mm)

    new_entry = {
        "timestamp": timestamp_dt.isoformat(),
        "date": timestamp_dt.strftime("%Y-%m-%d"),
        "hour": timestamp_dt.hour,
        "temp": t_now,
        "wind": wind_kmh,
        "rain": rain_mm,
        "status": status,
        "humidity": humidity,
        "pressure": pressure,
        "delta_t": delta_t,
        "foraging_intensity": intensity
    }

    # 2. Load Existing Data
    telemetry = load_json(TELEMETRY_FILE)
    archive = load_json(ARCHIVE_FILE)

    # 3. Daily Archive Rollover (Local Midnight)
    if telemetry and telemetry[-1]['date'] != new_entry['date']:
        yesterday_date = telemetry[-1]['date']
        yesterday_data = [i for i in telemetry if i['date'] == yesterday_date]
        
        if yesterday_data:
            t_max = max(float(i['temp']) for i in yesterday_data)
            t_min = min(float(i['temp']) for i in yesterday_data)
            avg_p = sum(float(i['pressure']) for i in yesterday_data) / len(yesterday_data)
            avg_h = sum(float(i['humidity']) for i in yesterday_data) / len(yesterday_data)
            total_r = sum(float(i['rain']) for i in yesterday_data)
            
            daily_gdd = max(((t_max + t_min) / 2) - BASE_TEMP, 0)
            last_cumulative = archive[-1]['cumulative_gdd'] if archive else 0
            
            optimal_slots = sum(1 for i in yesterday_data if i['status'] == "Optimal")
            flight_hours = optimal_slots * 3 # Estimation
            
            # Prevent duplicate date entries in archive
            if not any(a['date'] == yesterday_date for a in archive):
                archive.append({
                    "date": yesterday_date,
                    "t_max": t_max,
                    "t_min": t_min,
                    "avg_pressure": round(avg_p, 1),
                    "total_rain": round(total_r, 1),
                    "avg_humidity": round(avg_h, 1),
                    "daily_gdd": round(daily_gdd, 2),
                    "cumulative_gdd": round(last_cumulative + daily_gdd, 2),
                    "flight_hours": flight_hours,
                    "avg_delta_t": round(sum(float(i.get('delta_t', 0)) for i in yesterday_data) / len(yesterday_data), 1)
                })
            
            if len(archive) > MAX_ARCHIVE:
                archive = archive[-MAX_ARCHIVE:]
                
            with open(ARCHIVE_FILE, 'w') as f:
                json.dump(archive, f, indent=2)

    # 4. Telemetry Update (Overwrite if same hour/date exists)
    # This keeps our timeline clean and duplicate-free
    telemetry = [i for i in telemetry if not (i['date'] == new_entry['date'] and i.get('hour') == new_entry['hour'])]
    telemetry.append(new_entry)
    telemetry.sort(key=lambda x: x['timestamp'])
    
    # Calculate Rolling GDD using sliding 24-hour window
    now_dt = timestamp_dt
    window_start = now_dt - timedelta(hours=24)
    window = [i for i in telemetry if datetime.fromisoformat(i['timestamp']).replace(tzinfo=None) >= window_start]
    
    if window:
        r_max = max(float(i['temp']) for i in window)
        r_min = min(float(i['temp']) for i in window)
        new_entry['rolling_gdd'] = round(max(((r_max + r_min) / 2) - BASE_TEMP, 0), 2)
    else:
        new_entry['rolling_gdd'] = 0

    # 5. Maintain Buffer & Save
    if len(telemetry) > MAX_TELEMETRY:
        telemetry = telemetry[-MAX_TELEMETRY:]
        
    with open(TELEMETRY_FILE, 'w') as f:
        json.dump(telemetry, f, indent=2)

    print(f"Successfully updated {new_entry['timestamp']}. Hour: {new_entry.get('hour')}")

if __name__ == "__main__":
    update_stores()
