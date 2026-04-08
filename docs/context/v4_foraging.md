For the **Foraging Window**, you should absolutely keep the **3-hourly resolution** in your telemetry, but use a **"Daily Score"** for your archive. 

Think of it like a "Performance Metric" for a cloud service: you want the real-time logs (3-hourly) to see *when* it was down, and the daily SLA (archive) to see *how good* the day was overall.

---

### 1. Telemetry Level (3-Hourly): The "Traffic Light"
On your main dashboard ("Wylotek"), this should be a **Status Ribbon** or a **Gantt-style bar** for the last 24–48 hours.

* **Logic:** Every 3 hours, the script evaluates `is_flyable`.
* **Visualization:** A horizontal bar divided into 3-hour blocks.
    * **Green:** Optimal (Temp > 14°C, Wind < 20km/h, No Rain).
    * **Yellow:** Marginal (e.g., Temp 12-14°C or Wind 20-25km/h).
    * **Red:** Restricted (Rain or < 10°C).
* **Why:** This tells your friend: *"The bees had a 6-hour window this morning before the wind picked up."*

---

### 2. Archive Level (Daily): The "Foraging Hours" Score
In your `archive.json`, you want to quantify the day’s potential. This is a massive "Senior Beekeeper" metric for predicting honey yields.

* **Calculation:**
    ```python
    # Count how many 3-hour slots were 'Optimal'
    daily_foraging_slots = sum(1 for i in yesterday_data if i['status'] == "Optimal")
    # Each slot represents 3 hours
    foraging_hours = daily_foraging_slots * 3 
    ```
* **Visualization:** A simple **Bar Chart** in the archive section.
* **The Insight:** If the GDD is high (flowers are blooming) but the "Foraging Hours" bar is low (it was rainy/windy), your friend knows the bees are likely **starving** despite the flowers being out. This is the "Hunger Gap" warning.

---

### 🛠️ Execution: Update to `archive.json` logic
Add this to the rollover section of your Python script:

```python
if yesterday_data:
    # ... previous GDD logic ...
    
    # Calculate total flight hours for the day
    optimal_slots = [i for i in yesterday_data if i.get('status') == "Optimal"]
    flight_hours = len(optimal_slots) * 3 
    
    archive.append({
        "date": yesterday_date,
        "daily_gdd": round(daily_gdd, 2),
        "cumulative_gdd": round(last_cumulative + daily_gdd, 2),
        "flight_hours": flight_hours, # New Metric
        "avg_delta_t": round(sum(i.get('delta_t', 0) for i in yesterday_data) / len(yesterday_data), 1)
    })
```

---

### 🎨 Summary Recommendation for Astro

1.  **Live:** A "Current Status" badge: **"Foraging: Optimal"** (with a green pulse).
2.  **Short-Term:** A 24-hour "Timeline" bar showing the green/red blocks.
3.  **Long-Term:** A bar chart in the "Season View" showing **Flight Hours vs. GDD**. 



**The Execution Tip:** When the **GDD Line** goes up but the **Flight Hours Bar** stays at zero for 3 days, trigger a CSS alert in Astro: **"⚠️ Risk of Starvation: High Bloom / No Flight."** This is the kind of "Expert Guide" feature that makes a dashboard truly indispensable.