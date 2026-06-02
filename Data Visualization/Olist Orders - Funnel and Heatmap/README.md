# Olist Orders — Heatmap and Funnel Chart of the Logistics Process

Exploratory analysis of the logistics process of **Olist**, the largest e-commerce platform in Brazil, through interactive visualizations that identify patterns in order statuses and delivery flow stages.

---

## Problem Context

On which days of the week are orders most concentrated by status? How many orders complete each stage of the logistics process? At which stage do the greatest losses occur?

This analysis answers these questions through a heatmap and a funnel chart built with **Plotly**.

---

## Project Structure

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

- **Source:** [Brazilian E-Commerce Public Dataset — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **File used:** `olist_orders_dataset.csv`
- **Key variables:** `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_status`

---

## Technologies Used

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-purple?logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

---

## Methodology

1. **Initial load and exploration** — structure, data types, first rows
2. **Preprocessing:**
   - Converting time columns to datetime format
   - Extracting day of the week from `order_purchase_timestamp`
   - Creating boolean stage indicators
3. **Visualizations** — 3 interactive charts with Plotly

---

## Analysis and Findings

### Heatmap — All Statuses
Visualization of the number of orders by day of the week and order status, showing the general distribution of the logistics flow.

### Heatmap — Filtered Statuses
The most relevant statuses of the main flow are filtered: `approved`, `shipped`, `delivered` and `canceled`, for a clearer reading of patterns.

### Funnel Chart — Process Stages
Measurement of how many orders reach each stage:
- Purchased — order created
- Approved — payment approved
- Handed to Carrier — shipped to logistics operator
- Delivered to Customer — final delivery

---

## Main Conclusions

- The majority of orders concentrate in the **delivered** status throughout all days of the week, indicating a high level of logistics process fulfillment
- **Monday to Wednesday** show higher volumes of delivered orders
- The **funnel chart** shows a progressive reduction at each stage, with the greatest loss between shipping and final delivery
- Canceled orders represent a smaller but consistent proportion throughout the week

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
jupyter notebook Heatmap_Funnel_Acuna.ipynb
```

> The `olist_orders_dataset.csv` file must be in the same folder as the notebook.

---

## Author

**Juan Bautista Acuña**
Data Analyst | SQL · Python · Power BI
[GitHub](https://github.com/bautistaacuna) · [Email](mailto:bautistaacuna@gmail.com)
