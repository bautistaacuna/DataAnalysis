# AdventureWorks Data Analytics Project

## Overview
End-to-end data analytics project using the AdventureWorks dataset.
Covers ETL pipeline, SQL business analysis, machine learning, and dashboards.

## Tech Stack
- **Database**: PostgreSQL
- **ETL**: Python (pandas, SQLAlchemy)
- **SQL**: DBeaver
- **ML**: scikit-learn
- **Visualization**: Power BI, Tableau

## Project Structure

```
AdventureWorks/
├── etl_pipeline.py       # ETL pipeline: CSV → PostgreSQL
├── sql/
│   └── queries.sql       # Business analysis queries
├── notebooks/
│   ├── sales_forecast.ipynb      # Sales forecasting model
│   └── reseller_risk.ipynb       # Churn detection model
├── adventureworks_dashboard.pbix # Power BI dashboard
├── adventureworks_tableau.twbx   # Tableau dashboard
└── README.md
```

## Stages

### Stage 1 — SQL Business Analysis
Answered key business questions using CTEs, Window Functions, RANK and LAG:
- Sales evolution by year, quarter and month
- Most profitable product categories and margins
- Top resellers and churned resellers
- Salesperson performance vs quota

### Stage 2 — ETL Pipeline
Python pipeline that extracts pipe-separated CSVs, transforms and loads them into a PostgreSQL data warehouse with star schema (Kimball).

### Stage 3 — Machine Learning
- **Sales Forecast** — Linear Regression model predicting next 12 months
- **Reseller Churn Detection** — Random Forest classifier with 72% accuracy

### Stage 4 — Dashboards
- **Power BI** — Interactive dashboard with KPIs, year filter and sales analysis
- **Tableau** — Published dashboard on Tableau Public

## Tableau Dashboard
[View on Tableau Public](https://public.tableau.com/app/profile/juan.bautista.acuna/viz/adventureworks_tableau/AdventureWorksDashboard)

## Key Findings
- Sales grew from ~$500K/month in 2011 to ~$1.8M/month by end of 2013
- Bikes represent 95%+ of total internet sales revenue
- 23% reseller churn rate — low order value is the strongest churn predictor
- Linda Mitchell is the top salesperson with $10.3M in reseller sales