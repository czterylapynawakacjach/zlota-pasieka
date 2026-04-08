import json
from datetime import datetime

def clean_data():
    with open('src/data/telemetry.json', 'r') as f:
        telemetry = json.load(f)
    
    # Sort by timestamp
    telemetry.sort(key=lambda x: x['timestamp'])
    
    # Remove entries that are too close to each other (e.g. within 1 hour)
    # or just keep it simple and keep all sorted entries for now to see if it fixes the "gap"
    
    with open('src/data/telemetry.json', 'w') as f:
        json.dump(telemetry, f, indent=2)
    
    print("Sorted telemetry.json by timestamp.")

if __name__ == "__main__":
    clean_data()
