# Screen Time, Productivity and Attention Span

Exploratory analysis of the relationship between screen time, productivity and attention span across students and professionals, through interactive visualizations built with Plotly.

---

## Problem Context

Is there a relationship between screen time and attention span? Does the type of app used influence productivity? How does notification handling affect attention and productivity? Are there differences between students and professionals?

This analysis answers these questions through 12 interactive charts.

---

## Project Structure

```
Screen Time Data Productivity and Attention Span/
├── README.md
├── Screen_Time_Data_Productivity_and_Attention_Span.ipynb
├── data.csv
├── barplot_tiempo_pantalla.png
├── boxplot_atencion_pantalla.png
├── boxplot_productividad_pantalla.png
├── barplot_notificaciones_productividad.png
├── barplot_estrategia_atencion.png
├── barplot_edad_pantalla.png
├── barplot_notificaciones_atencion.png
├── boxplot_notificaciones_atencion.png
├── heatmap_horario_notificaciones.png
├── boxplot_productividad_notificaciones.png
├── barplot_app_atencion.png
└── barplot_heavy_users.png
```

---

## Dataset

- **Source:** [Screen Time Data — Kaggle](https://www.kaggle.com/datasets/mexwell/screen-time-and-productivity)
- **File used:** `data.csv`
- **Records:** 200 participants from different age groups, occupations and usage patterns
- **Key variables:** `Average Screen Time`, `Screen_Time_Hours`, `Attention_Score`, `Productivity_Score`, `Notification Handling`, `Work Strategy`, `Age Group`, `Occupation`, `App Category`

---

## Technologies Used

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

---

## Methodology

1. **Initial load and exploration** — structure, data types, first rows
2. **Data preparation** — null value handling, removal of unnecessary columns
3. **Variable transformation:**
   - `Average Screen Time` → numeric ordinal variable
   - `Attention Span` → numeric ordinal variable
   - `Productivity` → numeric ordinal variable
   - `Age Group`, `Education Level` → ordered categories
4. **Charts and correlations** — 12 interactive visualizations with Plotly

---

## Analysis and Findings

| Section | Analysis |
|---|---|
| 5.1 | Correlation: screen time vs attention span |
| 5.2 | Correlation: screen time vs productivity |
| 5.3 | Average screen time by age group |
| 5.4 | Screen usage period vs attention span |
| 5.5 | Productivity vs notification handling |
| 5.6 | Work strategy vs attention span |
| 5.7 | Distribution of daily screen time |
| 5.8 | Boxplot: screen time vs attention span |
| 5.9 | Boxplot: screen time vs productivity |
| 5.10 | Barplot: notification handling vs productivity |
| 5.11 | Barplot: work strategy vs attention span |
| 5.12 | Barplot: age group vs screen time |
| 5.13 | Heatmap: usage period vs notification handling |
| 5.14 | Boxplot: productivity vs notification handling |
| 5.16 | Barplot: app category vs attention span |
| 5.20 | Heavy Users vs Light Users |

---

## Main Conclusions

- There is **no significant correlation** between screen time and attention span or productivity
- **Notification handling** is the factor that most impacts productivity: those who ignore them until completing a task show better performance
- **Productivity apps** do not guarantee better results on their own
- **Professionals** spend more hours in front of screens than students, but both groups show similar attention and productivity levels
- Screen use oriented toward **academic or work tasks** is associated with higher attention than entertainment use
- **Young adults (25–34)** are the group with the highest daily digital exposure

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
jupyter notebook Screen_Time_Data_Productivity_and_Attention_Span.ipynb
```

> The `data.csv` file must be in the same folder as the notebook.

---

## Author

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
