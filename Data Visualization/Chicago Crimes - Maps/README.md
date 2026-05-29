# Chicago Crimes 2026 — Análisis Geolocalizado de Incidentes Delictivos

Análisis exploratorio de los incidentes delictivos reportados en la Ciudad de Chicago durante el año 2026, a través de visualizaciones geolocalizadas e interactivas construidas con Plotly Express.

## Contexto del problema

¿En qué zonas de Chicago se concentran los delitos? ¿Cuáles son los tipos de crimen más frecuentes? ¿Existen diferencias espaciales entre incidentes con y sin arresto? ¿Los delitos nocturnos se ubican en zonas distintas a los diurnos?

Este análisis responde esas preguntas a través de 4 mapas interactivos geolocalizados.


## Estructura del proyecto

```
Chicago Crimes - Maps/
├── README.md
├── Visualización_de_datos_geolocalizados_Chicago_crimes_2026.ipynb
├── Crimes_Chicago_2026.csv
├── mapa_todos_los_crimenes.html
├── mapa_top5_crimenes.html
├── mapa_arrestos.html
└── mapa_dia_noche.html
```

## Dataset

- **Fuente:** [Chicago Data Portal — City of Chicago](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
- **Archivo utilizado:** `Crimes_Chicago_2026.csv`
- **Período:** Año 2026 (hasta el 20 de enero)
- **Variables clave:** `Primary Type`, `Latitude`, `Longitude`, `Arrest`, `Domestic`, `Date`, `Location Description`


## Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualización-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)


## Metodología

1. **Carga y exploración inicial** — estructura, tipos de datos, primeras filas
2. **Limpieza de datos:**
   - Eliminación de filas sin coordenadas de latitud y/o longitud (0.36% del total)
   - Conversión de `Latitude` y `Longitude` de tipo objeto a numérico
   - Conversión de la variable `Date` a formato datetime
3. **Creación de variable `time_of_day`** — clasificación de incidentes en diurnos (06:00–18:00) y nocturnos (18:00–06:00)
4. **Visualizaciones** — 4 mapas interactivos con Plotly Express


## Mapas interactivos

> Los mapas están exportados como HTML. Descargalos y abrilos en tu navegador para verlos con toda la interactividad.

| Mapa | Descripción | Archivo |
|---|---|---|
| 4.1 | Todos los tipos de delito | `mapa_todos_los_crimenes.html` |
| 4.2 | Top 5 tipos de delito más frecuentes | `mapa_top5_crimenes.html` |
| 4.3 | Incidentes con y sin arresto | `mapa_arrestos.html` |
| 4.4 | Incidentes diurnos vs nocturnos | `mapa_dia_noche.html` |


## Conclusiones principales

- Los incidentes delictivos **no se distribuyen uniformemente** en Chicago, sino que forman hotspots en zonas de alta densidad urbana
- Los **5 delitos más frecuentes** (Theft, Battery, Motor Vehicle Theft, Assault y Deceptive Practice) coexisten en las mismas zonas de mayor actividad
- Los **incidentes sin arresto son más frecuentes** y se distribuyen ampliamente, mientras que los arrestos se concentran en zonas específicas
- Los **delitos nocturnos se concentran con mayor intensidad** en determinados sectores, mientras que los diurnos muestran una distribución más homogénea
- La visualización geolocalizada demuestra el valor de las herramientas interactivas para el análisis exploratorio del crimen urbano


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
jupyter notebook "Visualización_de_datos_geolocalizados_Chicago_crimes_2026.ipynb"
```

> El archivo `Crimes_Chicago_2026.csv` debe estar en la misma carpeta que el notebook.


## Autor

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
