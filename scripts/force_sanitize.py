import json
from datetime import datetime

def force_sanitize():
    with open('src/data/telemetry.json', 'r') as f:
        telemetry = json.load(f)
    
    sanitized = {}
    for entry in telemetry:
        # Parse timestamp, strictly removing 'Z' and any microsecond/minute noise
        raw_ts = entry['timestamp'].replace('Z', '')
        # Handle cases like 2026-04-03T08:36:30.514445
        if '.' in raw_ts:
            raw_ts = raw_ts.split('.')[0]
        
        dt = datetime.fromisoformat(raw_ts)
        # Force to full hour
        rounded_dt = dt.replace(minute=0, second=0, microsecond=0)
        key = rounded_dt.isoformat()
        
        # Standardize entry fields
        entry['timestamp'] = key
        entry['date'] = rounded_dt.strftime("%Y-%m-%d")
        entry['hour'] = rounded_dt.hour
        
        # Deduplicate: Keep latest entry for this specific hour
        sanitized[key] = entry
    
    # Back to list, sorted
    new_telemetry = [sanitized[k] for k in sorted(sanitized.keys())]
    
    with open('src/data/telemetry.json', 'w') as f:
        json.dump(new_telemetry, f, indent=2)
    
    print(f"Force Sanitization Complete. Unique hours: {len(new_telemetry)}")

if __name__ == "__main__":
    force_sanitize()
