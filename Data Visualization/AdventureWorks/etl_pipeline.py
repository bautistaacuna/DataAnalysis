"""
AdventureWorks ETL Pipeline
============================
Extracts data from CSV files, transforms it and loads it into PostgreSQL.

Usage:
    python etl_pipeline.py
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
import time

# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = r"C:\Users\Juan\Documents\AdventureWorks\data"

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "adventureworks",
    "user":     "postgres",
    "password": "1132" 
}

# ============================================================
# COLUMN DEFINITIONS (CSVs have no headers)
# ============================================================

COLUMNS = {
    "DimDate": [
        "date_key", "full_date", "day_number_of_week", "english_day_name",
        "spanish_day_name", "french_day_name", "day_number_of_month",
        "day_number_of_year", "week_number_of_year", "english_month_name",
        "spanish_month_name", "french_month_name", "month_number_of_year",
        "calendar_quarter", "calendar_year", "calendar_semester",
        "fiscal_quarter", "fiscal_year", "fiscal_semester"
    ],
    "DimGeography": [
        "geography_key", "city", "state_province_code", "state_province_name",
        "country_region_code", "english_country_region_name",
        "spanish_country_region_name", "french_country_region_name",
        "postal_code", "sales_territory_key", "ip_address_locator"
    ],
    "DimSalesTerritory": [
        "sales_territory_key", "sales_territory_alternate_key",
        "sales_territory_region", "sales_territory_country",
        "sales_territory_group", "sales_territory_image"  # excluded below
    ],
    "DimProductCategory": [
        "product_category_key", "product_category_alternate_key",
        "english_product_category_name", "spanish_product_category_name",
        "french_product_category_name"
    ],
    "DimProductSubcategory": [
        "product_subcategory_key", "product_subcategory_alternate_key",
        "english_product_subcategory_name", "spanish_product_subcategory_name",
        "french_product_subcategory_name", "product_category_key"
    ],
    "DimProduct": [
        "product_key", "product_alternate_key", "product_subcategory_key",
        "weight_unit_measure_code", "size_unit_measure_code",
        "english_product_name", "spanish_product_name", "french_product_name",
        "standard_cost", "finished_goods_flag", "color", "safety_stock_level",
        "reorder_point", "list_price", "size", "size_range", "weight",
        "days_to_manufacture", "product_line", "dealer_price", "class",
        "style", "model_name", "large_photo",   # large_photo excluded below
        "english_description", "french_description", "chinese_description",
        "arabic_description", "hebrew_description", "thai_description",
        "german_description", "japanese_description", "turkish_description",
        "start_date", "end_date", "status"
    ],
    "DimCustomer": [
        "customer_key", "geography_key", "customer_alternate_key", "title",
        "first_name", "middle_name", "last_name", "name_style", "birth_date",
        "marital_status", "suffix", "gender", "email_address", "yearly_income",
        "total_children", "number_children_at_home", "english_education",
        "spanish_education", "french_education", "english_occupation",
        "spanish_occupation", "french_occupation", "house_owner_flag",
        "number_cars_owned", "address_line1", "address_line2", "phone",
        "date_first_purchase", "commute_distance"
    ],
    "DimEmployee": [
        "employee_key", "parent_employee_key", "employee_national_id_alternate_key",
        "parent_employee_national_id", "sales_territory_key", "first_name",
        "last_name", "middle_name", "name_style", "title", "hire_date",
        "birth_date", "login_id", "email_address", "phone", "marital_status",
        "emergency_contact_name", "emergency_contact_phone", "salaried_flag",
        "gender", "pay_frequency", "base_rate", "vacation_hours",
        "sick_leave_hours", "current_flag", "sales_person_flag",
        "department_name", "start_date", "end_date", "status",
        "employee_photo"   # excluded below
    ],
    "DimReseller": [
        "reseller_key", "geography_key", "reseller_alternate_key", "phone",
        "business_type", "reseller_name", "number_employees", "order_frequency",
        "order_month", "first_order_year", "last_order_year", "product_line",
        "address_line1", "address_line2", "annual_sales", "bank_name",
        "min_payment_type", "min_payment_amount", "annual_revenue", "year_opened"
    ],
    "FactResellerSales": [
        "product_key", "order_date_key", "due_date_key", "ship_date_key",
        "reseller_key", "employee_key", "promotion_key", "currency_key",
        "sales_territory_key", "sales_order_number", "sales_order_line_number",
        "revision_number", "order_quantity", "unit_price", "extended_amount",
        "unit_price_discount_pct", "discount_amount", "product_standard_cost",
        "total_product_cost", "sales_amount", "tax_amt", "freight",
        "carrier_tracking_number", "customer_po_number",
        "order_date", "due_date", "ship_date"
    ],
    "FactInternetSales": [
        "product_key", "order_date_key", "due_date_key", "ship_date_key",
        "customer_key", "promotion_key", "currency_key", "sales_territory_key",
        "sales_order_number", "sales_order_line_number", "revision_number",
        "order_quantity", "unit_price", "extended_amount",
        "unit_price_discount_pct", "discount_amount", "product_standard_cost",
        "total_product_cost", "sales_amount", "tax_amt", "freight",
        "carrier_tracking_number", "customer_po_number",
        "order_date", "due_date", "ship_date"
    ],
    "FactSalesQuota": [
        "sales_quota_key", "employee_key", "date_key", "calendar_year",
        "calendar_quarter", "sales_amount_quota", "date"
    ]
}

# Columns to drop before loading (binary data)
DROP_COLUMNS = {
    "DimSalesTerritory": ["sales_territory_image"],
    "DimProduct":        ["large_photo"],
    "DimEmployee":       ["employee_photo"]
}

# Load order respects foreign key dependencies
LOAD_ORDER = [
    ("DimDate",             "dw.dim_date"),
    ("DimGeography",        "dw.dim_geography"),
    ("DimSalesTerritory",   "dw.dim_sales_territory"),
    ("DimProductCategory",  "dw.dim_product_category"),
    ("DimProductSubcategory","dw.dim_product_subcategory"),
    ("DimProduct",          "dw.dim_product"),
    ("DimCustomer",         "dw.dim_customer"),
    ("DimEmployee",         "dw.dim_employee"),
    ("DimReseller",         "dw.dim_reseller"),
    ("FactResellerSales",   "dw.fact_reseller_sales"),
    ("FactInternetSales",   "dw.fact_internet_sales"),
    ("FactSalesQuota",      "dw.fact_sales_quota"),
]

# ============================================================
# ETL FUNCTIONS
# ============================================================

def get_engine(config):
    """Create SQLAlchemy engine for PostgreSQL."""
    url = (
        f"postgresql+psycopg2://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
    )
    return create_engine(url)


def extract(file_name, columns):
    """Read CSV file with pipe separator and assign column names."""
    path = os.path.join(DATA_PATH, f"{file_name}.csv")
    df = pd.read_csv(
        path,
        sep="|",
        header=None,
        names=columns,
        usecols=range(len(columns)),  # ignora columnas extra si el CSV tiene más
        low_memory=False,
        encoding="utf-8",
        on_bad_lines="skip"
    )
    print(f"  Extracted {len(df):,} rows from {file_name}.csv")
    return df


def transform(df, file_name):
    """Clean and prepare data for loading."""

    # Drop binary columns
    if file_name in DROP_COLUMNS:
        df = df.drop(columns=DROP_COLUMNS[file_name], errors="ignore")

    # Replace empty strings with None
    df = df.replace("", None)

# Convert boolean columns
    bool_cols = {
        "DimCustomer":  ["name_style"],
        "DimEmployee":  ["name_style", "salaried_flag", "current_flag", "sales_person_flag"],
        "DimProduct":   ["finished_goods_flag"],
    }
    if file_name in bool_cols:
        for col in bool_cols[file_name]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    print(f"  Transformed {file_name}: {df.shape[0]:,} rows x {df.shape[1]} columns")
    # Drop rows with null values in critical columns
    if file_name == "DimSalesTerritory":
        df = df.dropna(subset=["sales_territory_region"])
    if file_name == "DimEmployee":
        df = df.dropna(subset=["first_name"])
    return df


def load(df, table_name, engine):
    """Load DataFrame into PostgreSQL table."""
    schema, tbl = table_name.split(".")
    with engine.begin() as conn:
        conn.execute(text("SET session_replication_role = replica;"))
        df.to_sql(
            name=tbl,
            con=conn,
            schema=schema,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )
        conn.execute(text("SET session_replication_role = DEFAULT;"))
    print(f"  Loaded into {table_name} ✓")


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_pipeline():
    print("=" * 60)
    print("AdventureWorks ETL Pipeline")
    print("=" * 60)

    # Connect to database
    print("\nConnecting to PostgreSQL...")
    engine = get_engine(DB_CONFIG)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connection successful ✓")

    total_start = time.time()

    for file_name, table_name in LOAD_ORDER:
        print(f"\n--- Processing {file_name} ---")
        start = time.time()
        try:
            df = extract(file_name, COLUMNS[file_name])
            df = transform(df, file_name)
            load(df, table_name, engine)
            elapsed = time.time() - start
            print(f"  Done in {elapsed:.1f}s")
        except Exception as e:
            print(f"  ERROR: {e}")

    total_elapsed = time.time() - total_start
    print(f"\n{'=' * 60}")
    print(f"Pipeline completed in {total_elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
