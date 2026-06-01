# Chicago Crimes 2026 — Geolocalized Analysis of Criminal Incidents

Exploratory analysis of criminal incidents reported in the City of Chicago during 2026, through geolocalized and interactive visualizations built with Plotly Express.

---

## Problem Context

In which areas of Chicago are crimes concentrated? Which are the most frequent crime types? Are there spatial differences between incidents with and without arrest? Do nighttime crimes occur in different areas than daytime ones?

This analysis answers these questions through 4 geolocalized interactive maps.

---

## Project Structure

```
Chicago Crimes - Maps/
├── README.md
├── Chicago_Crimes_2026.ipynb
├── Crimes_Chicago_2026.csv
├── mapa_todos_los_crimenes.html
├── mapa_top5_crimenes.html
├── mapa_arrestos.html
└── mapa_dia_noche.html
```

---

## Dataset

- **Source:** [Chicago Data Portal — City of Chicago](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
- **File used:** `Crimes_Chicago_2026.csv`
- **Period:** 2026 (up to January 20)
- **Key variables:** `Primary Type`, `Latitude`, `Longitude`, `Arrest`, `Domestic`, `Date`, `Location Description`

---

## Technologies Used

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

---

## Methodology

1. **Initial load and exploration** — structure, data types, first rows
2. **Data cleaning:**
   - Removal of rows without latitude and/or longitude coordinates (0.36% of total)
   - Conversion of `Latitude` and `Longitude` from object to numeric type
   - Conversion of the `Date` variable to datetime format
3. **Creation of `time_of_day` variable** — classification of incidents into daytime (06:00–18:00) and nighttime (18:00–06:00)
4. **Visualizations** — 4 interactive maps with Plotly Express

---

## View the Interactive Maps

> GitHub cannot render geolocalized interactive maps. To view them, download the HTML files and open them in your browser.

| Map | Description | File |
|---|---|---|
| 4.1 | All crime types | `mapa_todos_los_crimenes.html` |
| 4.2 | Top 5 most frequent crime types | `mapa_top5_crimenes.html` |
| 4.3 | Incidents with and without arrest | `mapa_arrestos.html` |
| 4.4 | Daytime vs nighttime incidents | `mapa_dia_noche.html` |

---

## Main Conclusions

- Criminal incidents **do not distribute uniformly** across Chicago, but form hotspots in high-density urban areas
- The **5 most frequent crimes** (Theft, Battery, Motor Vehicle Theft, Assault and Deceptive Practice) coexist in the same high-activity zones
- **Incidents without arrest are more frequent** and widely distributed, while arrests concentrate in specific areas
- **Nighttime crimes concentrate more intensely** in certain sectors, while daytime incidents show a more homogeneous distribution
- Geolocalized visualization demonstrates the value of interactive tools for exploratory urban crime analysis

---

## How to Run the Project

```bash
# 1. Clone the repository
git clone https://github.com/bautistaacuna/DataAnalysis.git

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Open the notebook
jupyter notebook Chicago_Crimes_2026.ipynb
```

> The `Crimes_Chicago_2026.csv` file must be in the same folder as the notebook.

---

## Author

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
