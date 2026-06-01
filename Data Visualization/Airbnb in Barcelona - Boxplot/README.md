# Airbnb Barcelona — Weekday Price Analysis

Exploratory analysis of the Airbnb accommodation market in Barcelona during weekdays, focusing on the relationship between price, accommodation type, location and service quality.

---

## Problem Context

What factors determine the price of an Airbnb listing in Barcelona? Does being a Superhost imply higher prices? Are more central accommodations always more expensive?

This analysis answers these questions through boxplots and scatter plots built with **Plotly**.

---

## Project Structure

```
Airbnb in Barcelona - Boxplot/
├── README.md
├── Airbnb_Barcelona.ipynb
├── barcelona_weekdays.csv
├── boxplot_precio_tipo.png
├── boxplot_precio_superhost.png
├── boxplot_limpieza_tipo.png
├── boxplot_distancia_centro.png
├── boxplot_distancia_metro.png
├── scatter_distancia_precio_satisfaccion.png
├── scatter_distancia_precio_limpieza.png
├── scatter_distancia_precio_superhost.png
├── scatter_distancia_precio_negocios.png
└── scatter_satisfaccion_precio.png
```

---

## Dataset

- **Source:** [Airbnb Prices in European Cities — Kaggle](https://www.kaggle.com/datasets/thedevastator/airbnb-prices-in-european-cities)
- **File used:** `barcelona_weekdays.csv`
- **Key variables:** `realSum`, `room_type`, `host_is_superhost`, `cleanliness_rating`, `guest_satisfaction_overall`, `dist`, `metro_dist`, `biz`

---

## Technologies Used

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

---

## Methodology

1. **Initial load and exploration** — data types, dimensions, first rows
2. **Data cleaning** — null values, duplicates and categorical variable transformation
3. **Descriptive analysis** — statistics grouped by accommodation type
4. **Visualizations** — 10 interactive charts with Plotly (boxplots and scatter plots)

---

## Analysis and Findings

### Boxplots

| Chart | Variable analyzed |
|---|---|
| 3.1 | Price by accommodation type |
| 3.2 | Price by Superhost status |
| 3.3 | Cleanliness score by accommodation type |
| 3.4 | Distance to city center by accommodation type |
| 3.5 | Distance to metro by accommodation type |

### Scatter Plots

| Chart | Variables |
|---|---|
| 3.6 | Distance vs Price — color: type, size: satisfaction |
| 3.7 | Distance vs Price — color: type, size: cleanliness |
| 3.8 | Distance vs Price — color: superhost, size: satisfaction |
| 3.9 | Distance vs Price — color: business travel, size: satisfaction |
| 3.10 | Satisfaction vs Price — color: type, size: cleanliness |

---

## Main Conclusions

- **Entire homes are the most expensive and most central**, with high price variability and extreme outliers (up to €6,943)
- **Being a Superhost does not determine a higher price**, but reflects consistency in the guest experience
- **Shared rooms are the most affordable and furthest from the center**, oriented toward budget tourism
- **Cleanliness and guest satisfaction do not show a strong relationship with price or distance**
- There are clearly **two market segments**: premium tourism (central entire homes) and budget tourism (more distant private/shared rooms)

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
jupyter notebook Airbnb_Barcelona.ipynb
```

> The `barcelona_weekdays.csv` file must be in the same folder as the notebook.

---

## Author

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
