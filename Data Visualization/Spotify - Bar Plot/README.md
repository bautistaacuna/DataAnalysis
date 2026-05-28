# Spotify Global Music Analysis (2009–2025)
Análisis exploratorio y visual del dataset global de Spotify, con foco en géneros musicales, tendencias temporales y los artistas más populares de la plataforma.

## Contexto del problema
¿Qué géneros musicales dominan Spotify? ¿Cómo evolucionó el contenido explícito a lo largo de los años? ¿Existe relación entre la popularidad de un artista y la cantidad de seguidores que tiene?

Este análisis responde esas preguntas a través de visualizaciones interactivas construidas con **Plotly**.

## Estructura del proyecto

```
Spotify - Bar/
├── Spotify.ipynb              # Notebook principal con el análisis completo
├── spotify_data clean.csv     # Dataset utilizado
└── README.md                  # Este archivo
```

## Dataset
- **Fuente:** [Spotify Global Music Dataset 2009–2025 — Kaggle](https://www.kaggle.com/datasets/wardabilal/spotify-global-music-dataset-20092025)
- **Registros:** Dataset global con canciones, artistas, géneros, popularidad y seguidores
- **Variables clave:** `artist_name`, `artist_genres`, `artist_popularity`, `artist_followers`, `track_name`, `track_popularity`, `explicit`, `album_release_date`

## Tecnologías utilizadas
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualización-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

## Metodología
1. **Carga y exploración inicial** — shape, dtypes, primeras filas
2. **Limpieza de datos:**
   - Conversión de `album_release_date` a datetime y extracción del año
   - Identificación y tratamiento de valores nulos
   - Eliminación de duplicados
   - Creación de columna `main_genre` a partir del primer género del artista
3. **Visualizaciones** — 5 gráficos interactivos con Plotly

## Análisis y hallazgos
### 1. Top 30 géneros musicales por cantidad de canciones
Gráfico de barras con los géneros más representados en el dataset, excluyendo entradas sin género clasificado.

### 2. Contenido explícito por género
Comparación del volumen de canciones explícitas vs no explícitas para los 30 géneros principales. Permite identificar qué géneros tienen mayor proporción de contenido explícito.

### 3. Evolución de lanzamientos por año
Serie temporal que muestra el crecimiento en la producción musical registrada en Spotify desde 2009 hasta 2025.

### 4. Lanzamientos explícitos vs no explícitos a lo largo del tiempo
Análisis de cómo fue variando la presencia de contenido explícito año a año, revelando una tendencia de crecimiento sostenido.

### 5. Top 20 artistas: seguidores vs popularidad (Bubble Chart)
Scatter plot multidimensional donde:
- **Eje X:** Cantidad de seguidores (escala logarítmica)
- **Eje Y:** Popularidad del artista (0–100)
- **Tamaño de burbuja:** Cantidad de canciones en el dataset
- **Color:** Género musical principal

## Conclusiones principales
- El **pop** y sus subgéneros dominan ampliamente la plataforma en cantidad de canciones
- El contenido explícito ha crecido de forma constante desde 2015, especialmente en géneros como **rap** y **hip-hop**
- No existe una correlación lineal perfecta entre seguidores y popularidad: artistas con menos seguidores pueden tener alta popularidad por reproducciones recientes
- La producción musical registrada en Spotify muestra un pico pronunciado entre 2020 y 2023

## Cómo ejecutar el proyecto
```bash
# 1. Clonar el repositorio
git clone https://github.com/bautistaacuna/DataAnalysis.git

# 2. Instalar dependencias
pip install pandas plotly

# 3. Abrir el notebook
jupyter notebook Spotify.ipynb
```

> El dataset `spotify_data clean.csv` debe estar en la misma carpeta que el notebook.

## Autor

**Juan Bautista Acuña**
Data Analyst | SQL • Python • Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
