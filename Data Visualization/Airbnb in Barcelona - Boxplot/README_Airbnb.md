# Airbnb Barcelona — Análisis de Precios en Días de Semana

Análisis exploratorio del mercado de alojamientos de Airbnb en Barcelona durante días de semana, con foco en la relación entre precio, tipo de alojamiento, ubicación y calidad del servicio.


## Contexto del problema

¿Qué factores determinan el precio de un alojamiento en Airbnb Barcelona? ¿Ser Superhost implica cobrar más? ¿Los alojamientos más céntricos son siempre los más caros?

Este análisis responde esas preguntas a través de boxplots y scatter plots construidos con **Plotly**.


## Estructura del proyecto

```
Airbnb in Barcelona - Boxplot/
├── Airbnb_Barcelona.ipynb         # Notebook principal con el análisis completo
├── barcelona_weekdays.csv         # Dataset utilizado
├── boxplot_precio_tipo.png
├── boxplot_precio_superhost.png
├── boxplot_limpieza_tipo.png
├── boxplot_distancia_centro.png
├── boxplot_distancia_metro.png
├── scatter_distancia_precio_satisfaccion.png
├── scatter_distancia_precio_limpieza.png
├── scatter_distancia_precio_superhost.png
├── scatter_distancia_precio_negocios.png
├── scatter_satisfaccion_precio.png
└── README.md
```

---

## Dataset

- **Fuente:** [Airbnb Prices in European Cities — Kaggle](https://www.kaggle.com/datasets/thedevastator/airbnb-prices-in-european-cities)
- **Archivo utilizado:** `barcelona_weekdays.csv`
- **Variables clave:** `realSum`, `room_type`, `host_is_superhost`, `cleanliness_rating`, `guest_satisfaction_overall`, `dist`, `metro_dist`, `biz`


## Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualización-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)


## Metodología

1. **Carga y exploración inicial** — tipos de datos, dimensiones, primeras filas
2. **Limpieza de datos** — revisión de nulos, duplicados y transformación de variables categóricas
3. **Análisis descriptivo** — estadísticas agrupadas por tipo de alojamiento
4. **Visualizaciones** — 10 gráficos interactivos con Plotly (boxplots y scatter plots)


## Análisis y hallazgos

### Boxplots

| Gráfico | Variable analizada |
|---|---|
| 3.1 | Precio según tipo de alojamiento |
| 3.2 | Precio según si el anfitrión es Superhost |
| 3.3 | Puntuación de limpieza según tipo de alojamiento |
| 3.4 | Distancia al centro según tipo de alojamiento |
| 3.5 | Distancia al metro según tipo de alojamiento |

### Scatter Plots

| Gráfico | Variables |
|---|---|
| 3.6 | Distancia vs Precio — color: tipo, tamaño: satisfacción |
| 3.7 | Distancia vs Precio — color: tipo, tamaño: limpieza |
| 3.8 | Distancia vs Precio — color: superhost, tamaño: satisfacción |
| 3.9 | Distancia vs Precio — color: viaje de negocios, tamaño: satisfacción |
| 3.10 | Satisfacción vs Precio — color: tipo, tamaño: limpieza |


## Conclusiones principales

- Los **alojamientos completos son los más caros y céntricos**, con alta variabilidad de precios y presencia de outliers extremos (hasta 6.943 €)
- Ser **Superhost no determina un precio mayor**, pero sí refleja consistencia en la experiencia del huésped
- Las **habitaciones compartidas son las más económicas y alejadas del centro**, orientadas a turismo de bajo presupuesto
- La **limpieza y satisfacción del huésped no muestran relación fuerte con el precio ni con la distancia**
- Existen claramente **dos segmentos de mercado**: turismo premium (alojamientos completos céntricos) y turismo económico (habitaciones privadas/compartidas más alejadas)


## Cómo ejecutar el proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/bautistaacuna/DataAnalysis.git

# 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Abrir el notebook
jupyter notebook Airbnb_Barcelona.ipynb
```

> El archivo `barcelona_weekdays.csv` debe estar en la misma carpeta que el notebook.


## Autor

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
