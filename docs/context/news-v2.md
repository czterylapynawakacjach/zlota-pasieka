This Markdown summary is designed for your agent to ingest. It follows the **"Bento Box"** UI strategy—mixing a high-level **Marquee** for awareness with a structured **Grid** for deep reading.

---

# 🐝 Implementation Spec: HiveOps News & "The Daily Buzz"

## 1. Data Ingestion Architecture
* **Source Logic:** Python script fetching from 3 buckets:
    * **RSS (Technical):** *Bee Culture*, *BeeLife EU*, *Radio Warroza*.
    * **Google News (Local):** Queries: `"pszczelarstwo Wołomin"`, `"cena miodu 2026"`.
    * **Static (Global):** Apimondia events & World Bee Day (May 20).
* **Storage:** `src/data/news.json` (Static build-time ingestion).
* **Frequency:** Daily build trigger via GitHub Actions.

---

## 2. Widget A: The "Live Ticker" (Global Marquee)
* **Placement:** Fixed at the very top of the site (`Header`).
* **UI Style:** * Background: `bg-amber-400/10` with `backdrop-blur-sm`.
    * Content: `[Source Name] Title — [Source Name] Title`.
* **Animation:** Modern CSS `translateX` loop (not the `<marquee>` tag).
* **Mobile Behavior:** Slow down speed by 20%; pause on touch.

---

## 3. Widget B: The "Bento News" Grid (Main Dashboard)
Replace the simple news list with a **Bento Grid** (Responsive Grid).
* **Hierarchy:** * **The "Big Tile" (2x2):** Most recent local news from Poland/Wołomin. Include a short summary and an "Alert" icon if keywords like "pesticide" or "subsidy" appear.
    * **The "Standard Tiles" (1x1):** RSS headlines with source icons.
* **Visual Polish:** * `Glassmorphism`: White cards with `bg-white/70` and `border-white/20`.
    * `Hover States`: Subtle amber glow (`shadow-[0_0_15px_rgba(251,191,36,0.4)]`).

---

## 4. Widget C: The "Interactive Stack" (Mobile Only)
When screen width is `< 768px`, collapse the Bento Grid into a **Stack Deck**.
* **UX:** Show only the top card. Users swipe left/right to see the next headline.
* **Benefit:** Keeps the mobile view clean for the weather charts while allowing news browsing.

---

## 5. Technical Requirements for Agent
1.  **Safety:** All news links must use `target="_blank"` and `rel="noopener noreferrer"`.
2.  **Performance:** News summaries must be truncated to **150 characters** in the JSON to keep the DOM light.
3.  **Empty State:** If `news.json` is empty or fetch fails, the widget should gracefully hide or display: *"No news today—bees are busy!"*
4.  **Polish Support:** Ensure `utf-8` encoding is strictly handled for characters like `ą, ć, ę, ł, ó, ś`.

---

### **Agent Action Prompt:**
> "Implement the HiveOps News Hub using a **Bento Grid** layout for the dashboard. Integrate a CSS-based **Marquee** for the header. Use `src/data/news.json` as the data source. Ensure the UI is responsive, moving to a **Stack Deck** on mobile. Style with a 'Glassmorphism' aesthetic and amber accent colors."