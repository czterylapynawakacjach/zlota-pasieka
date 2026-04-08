To keep your **Wylotek** dashboard clean and actionable for the beekeeper, here is the technical recommendation for the **Delta T** component.

---

### 📉 The Visualization: **"Nectar Flow Window"**
* **Type:** 7-Day **Line Chart** with a **Horizontal Range Band**.
* **X-Axis:** Date/Time (3-hourly intervals from `telemetry.json`).
* **Y-Axis:** Delta T ($\Delta T$) in °C.
* **The Range Band (The "Sweet Spot"):** Use a shaded background (e.g., light green) between **$2\text{°C}$ and $8\text{°C}$**.

### 🧠 The Logic (The "Why")
| Delta T Value | Visual Feedback | Meaning for the Bees |
| :--- | :--- | :--- |
| **$< 2\text{°C}$** | **Blue/Cold** | Air is too damp; nectar is watery/dilute. |
| **$2\text{--}8\text{°C}$** | **Green/Optimal** | **Perfect Flow.** Nectar is at the ideal viscosity for suction. |
| **$> 10\text{°C}$** | **Red/Dry** | Nectar is "caramelizing" or drying up; flowers stop secreting. |



---

### 🛠️ Execution: The Python Calculation
Add this single line to your `update_stores` function to generate the metric:

```python
# Simplified Delta T approximation using Dry Temp and Relative Humidity
# Formula: Delta T = T_dry * (1 - (RH / 100))
humidity = float(raw_data['wilgotnosc_wzgledna'])
delta_t = t_now * (1 - (humidity / 100))

new_entry = {
    # ... other fields ...
    "delta_t": round(delta_t, 1),
}
```

---

### 🎨 Execution: The Astro UI
In your Chart.js or Tailwind/SVG component:
1.  **Plot the `delta_t` line** in a neutral color (e.g., dark gray or purple).
2.  **Add a `plugins: { annotation: { ... } }`** (if using Chart.js) to draw the green box from 2 to 8.
3.  **Add a "Status Label"** next to the chart:
    * If `current_delta_t` is in the band: **"Nectar: Flowing"**
    * If `current_delta_t > 10`: **"Nectar: Too Dry/Sticky"**
    * If `current_delta_t < 2`: **"Nectar: Too Dilute/Watery"**

### 🏁 Summary for the User
This chart tells the beekeeper exactly **when during the day** the bees are actually productive. If the line is sitting at $14\text{°C}$ Delta T on a hot Wołomin afternoon, the bees might be "bearding" outside the hive instead of foraging, because there is no liquid nectar left to collect.