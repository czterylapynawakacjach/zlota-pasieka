import json
from datetime import datetime

def sanitize_telemetry():
    with open('src/data/telemetry.json', 'r') as f:
        telemetry = json.load(f)
    
    sanitized = {}
    for entry in telemetry:
        # Parse timestamp
        dt = datetime.fromisoformat(entry['timestamp'].replace('Z', ''))
        # Round to the hour (measurement time)
        rounded_dt = dt.replace(minute=0, second=0, microsecond=0)
        key = rounded_dt.isoformat()
        
        # Update entry with standardized hour and date
        entry['timestamp'] = key
        entry['date'] = rounded_dt.strftime("%Y-%m-%d")
        entry['hour'] = rounded_dt.hour
        
        # Keep the latest entry for this hour (overwriting previous ones)
        sanitized[key] = entry
    
    # Convert back to sorted list
    new_telemetry = [sanitized[k] for k in sorted(sanitized.keys())]
    
    with open('src/data/telemetry.json', 'w') as f:
        json.dump(new_telemetry, f, indent=2)
    
    print(f"Sanitized telemetry. Unique hours: {len(new_telemetry)}")

if __name__ == "__main__":
    sanitize_telemetry()
