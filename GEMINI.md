<!-- AI_CONTEXT_START -->
# 🐝 Złota Pasieka - Technical Context & Handover

> **Note:** This file serves as the primary technical source of truth for AI agents. It should be updated at the end of every significant development session.
<!-- AI_CONTEXT_END -->

## 1. Project Overview & Goal
Standalone, modern, static, multilingual website for an educational apiary. This project provides a live "Bee-Ops" telemetry dashboard and informational pages about beekeeping.

## 2. Technical Stack
*   **Framework:** Astro (Static Site Generation)
*   **Styling:** Tailwind CSS (Utility-first)
*   **Typography:** Inter (Standard UI)
*   **Data Architecture**: 
    *   `telemetry.json`: 3-hourly high-resolution weather data (IMGW-PIB).
    *   `archive.json`: Daily summarized metrics (Seasonal trends).
    *   `news.json`: Daily aggregated beekeeping news (RSS + Google News).
*   **Diagrams:** Mermaid.js (Client-side rendering).
*   **Automation**: Python ETL scripts + GitHub Actions for 3-hourly weather sync and daily news sync.
*   **Hosting:** GitHub Pages (Subpath: `/zlota-pasieka/`).

## 3. Site Structure
*   **Home (`/`)**: Automatic redirect to `/pl/`.
*   **News Hub**: Top marquee ticker and Bento Grid news section.
*   **Bee-Ops Dashboard**: Real-time gauges and dual-axis Chart.js visualizations.
*   **Bee Cycle**: Vertical timeline of seasonal apiary events.
*   **Pantry**: Product showcase with mobile-optimized grid.

## 4. Architectural Mandates
*   **100% Static:** Must be buildable via `npm run build`.
*   **Subpath Aware:** All links and assets must respect the `base: '/zlota-pasieka'` config.
*   **Flattened Structure:** NO subfolders like `/v4/`. Components are in `src/components/`, layouts in `src/layouts/`.
*   **i18n Routing:** Direct `/[lang]/` routing (Polish/English).

## 5. Key Logic & Formulas
*   **Foraging Intensity:** Clamped 0-100%. 0 if Rain > 0 or Temp < 10°C. Half efficiency if Temp < 14°C.
*   **Delta T:** `temp * (1 - (humidity / 100))`. Optimal flow is 2°C - 8°C.
*   **GDD:** Growing Degree Days using 10°C base.
*   **Thermal Envelope:** Comparative current temp vs 24h rolling min/max.

## 6. Recent History & Handover
*   **Migration Complete:** Successfully extracted V4 from the portfolio repo into this standalone repo.
*   **Structure Flattened:** Corrected all relative imports (`i18n`, `data`, `components`) to match the new flat structure.
*   **News v2 Implemented:** Added global marquee ticker and responsive Bento Grid with Glassmorphism.
*   **Mobile Fixed:** Resolved zooming issues and horizontal overflow caused by background hex decor.
*   **Build & Deploy:** Configured GitHub Actions for weather sync (`data_sync.yml`), news sync (`news_sync.yml`), and deployment (`deploy.yml`).

## 7. Active Constraints
*   **Deployment:** Ensure GitHub Pages source is set to "GitHub Actions" in repo settings.
*   **Cursor:** Custom 🐝 cursor is global; standard cursor is hidden in CSS.
