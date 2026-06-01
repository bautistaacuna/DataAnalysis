# Olist Orders — Heatmap y Funnel Chart del Proceso Logístico

Análisis exploratorio del proceso logístico de **Olist**, la mayor plataforma de e-commerce de Brasil, a través de visualizaciones interactivas que permiten identificar patrones en los estados de los pedidos y las etapas del flujo de entrega.

---

## Contexto del problema

¿En qué días de la semana se concentran más pedidos según su estado? ¿Cuántos pedidos completan cada etapa del proceso logístico? ¿En qué etapa se producen las mayores pérdidas?

Este análisis responde esas preguntas a través de un heatmap y un funnel chart construidos con **Plotly**.

---

## Estructura del proyecto

```
Olist Orders - Funnel and Heatmap/
├── README.md
├── Heatmap_Funnel_Acuna.ipynb
├── olist_orders_dataset.csv
├── heatmap_pedidos_todos.png
├── heatmap_pedidos_filtrado.png
└── funnel_pedidos.png
```

---

## Dataset

- **Fuente:** [Brazilian E-Commerce Public Dataset — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Archivo utilizado:** `olist_orders_dataset.csv`
- **Variables clave:** `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_status`

---

## Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualización-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

---

## Metodología

1. **Carga y exploración inicial** — estructura, tipos de datos, primeras filas
2. **Preprocesamiento:**
   - Conversión de columnas de tiempo a formato datetime
   - Extracción del día de la semana desde `order_purchase_timestamp`
   - Creación de indicadores booleanos por etapa del proceso
3. **Visualizaciones** — 3 gráficos interactivos con Plotly

---

## Análisis y hallazgos

### Heatmap — Todos los estados
Visualización de la cantidad de pedidos por día de la semana y estado del pedido, mostrando la distribución general del flujo logístico.

### Heatmap — Estados filtrados
Se filtran los estados más relevantes del flujo principal: `approved`, `shipped`, `delivered` y `canceled`, para una lectura más clara de los patrones.

### Funnel Chart — Etapas del proceso
Medición de cuántos pedidos alcanzan cada etapa:
- Purchased — compra creada
- Approved — pago aprobado
- Shipped — enviado al transportista
- Delivered — entregado al cliente

---

## Conclusiones principales

- La mayoría de los pedidos se concentran en el estado **delivered** a lo largo de todos los días de la semana, lo que indica un alto nivel de cumplimiento del proceso logístico
- Los días de **lunes a miércoles** presentan mayor volumen de pedidos entregados
- El **funnel chart** muestra una reducción progresiva en cada etapa, con la mayor pérdida entre el envío y la entrega final
- Los pedidos cancelados representan una proporción menor pero constante a lo largo de la semana

---

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
jupyter notebook Heatmap_Funnel_Acuna.ipynb
```

> El archivo `olist_orders_dataset.csv` debe estar en la misma carpeta que el notebook.

---

## Autor

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
