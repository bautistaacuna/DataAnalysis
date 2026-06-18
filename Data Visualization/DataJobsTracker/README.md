# Data Jobs Market Tracker

Proyecto end-to-end de scraping, ETL y análisis del mercado laboral en Data Analytics / Engineering.

## Pipeline

```
Indeed Jobs → scraper.py → data/raw/*.csv
                              ↓
                         transform.py → data/processed/*.csv
                              ↓
                           load.py → PostgreSQL
                              ↓
                         analysis.sql → insights
                              ↓
                         visualize.py → charts/
```

## Stack

- **Scraping**: Python, requests, BeautifulSoup4
- **Transformación**: pandas, regex
- **Base de datos**: PostgreSQL, SQLAlchemy
- **Análisis**: SQL (CTEs, Window Functions)
- **Visualización**: matplotlib, seaborn, Plotly

## Uso

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Correr el scraper
python scraper.py

# 3. (próximas etapas)
python transform.py
python load.py
```

## Estructura

```
data_jobs_tracker/
├── scraper.py          # Etapa 1: recolección
├── transform.py        # Etapa 2: limpieza
├── load.py             # Etapa 3: carga a PostgreSQL
├── analysis.sql        # Etapa 4: queries de negocio
├── visualize.py        # Etapa 5: gráficos
├── requirements.txt
├── README.md
└── data/
    ├── raw/            # CSVs crudos del scraper
    └── processed/      # CSVs limpios
```
