"""
Data Jobs Market Tracker — Stage 3: Load to PostgreSQL
Input:  data/processed/jobs_clean_*.csv  (latest file)
Output: PostgreSQL table → adventureworks.dw.data_jobs_market

Uses SQLAlchemy to connect to the existing local PostgreSQL instance.
Credentials loaded from .env file.
"""

import pandas as pd
import logging
import os
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ── Load credentials ───────────────────────────────────────────────────────────
load_dotenv()

DB_USER     = os.getenv("DB_USER",     "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST     = os.getenv("DB_HOST",     "localhost")
DB_PORT     = os.getenv("DB_PORT",     "5432")
DB_NAME     = os.getenv("DB_NAME",     "adventureworks")
DB_SCHEMA   = os.getenv("DB_SCHEMA",   "dw")
TABLE_NAME  = "data_jobs_market"

PROCESSED_DIR = Path("data/processed")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Functions ──────────────────────────────────────────────────────────────────

def load_latest_clean() -> pd.DataFrame:
    """Loads the most recent cleaned CSV from data/processed/."""
    files = sorted(PROCESSED_DIR.glob("jobs_clean_*.csv"))

    if not files:
        raise FileNotFoundError("No clean CSV files found in data/processed/")

    latest = files[-1]
    log.info(f"Loading: {latest}")

    df = pd.read_csv(latest, encoding="utf-8-sig")
    log.info(f"Records loaded: {len(df)}")
    return df


def get_engine():
    """Creates and returns a SQLAlchemy engine for PostgreSQL."""
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)
    log.info(f"Connected to: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    return engine


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Final prep before loading to DB:
    - Convert boolean column to proper bool type
    - Ensure correct dtypes for salary columns
    - Add load timestamp
    """
    df = df.copy()

    # is_remote comes as True/False string from CSV — convert to bool
    if "is_remote" in df.columns:
        df["is_remote"] = df["is_remote"].map(
            {True: True, False: False, "True": True, "False": False}
        ).fillna(False).astype(bool)

    # salary columns — force numeric, coerce errors to NaN
    for col in ["salary_min", "salary_max", "salary_avg"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # add load timestamp
    df["loaded_at"] = datetime.now().isoformat()

    return df


def load_to_postgres(df: pd.DataFrame, engine) -> None:
    """
    Loads the DataFrame into PostgreSQL.
    Uses if_exists='replace' to recreate the table on each run.
    This keeps the data fresh — ideal for a market tracker updated daily.
    """
    full_table = f"{DB_SCHEMA}.{TABLE_NAME}"

    log.info(f"Loading {len(df)} records into {full_table}...")

    df.to_sql(
        name=TABLE_NAME,
        con=engine,
        schema=DB_SCHEMA,
        if_exists="replace",    # drops and recreates the table each run
        index=False,
        chunksize=500,          # insert in batches of 500 rows
    )

    log.info(f"Load complete.")


def verify_load(engine, schema: str, table: str) -> None:
    """Runs a quick count query to confirm the data loaded correctly."""
    query = text(f'SELECT COUNT(*) FROM "{schema}"."{table}"')

    with engine.connect() as conn:
        result = conn.execute(query).scalar()
        log.info(f"Verification — rows in {schema}.{table}: {result}")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Data Jobs Market Tracker — Stage 3: Load to PostgreSQL")

    # 1. Load clean data
    df = load_latest_clean()

    # 2. Connect to DB
    engine = get_engine()

    # 3. Prepare dataframe
    df = prepare_dataframe(df)
    log.info(f"Columns to load: {list(df.columns)}")

    # 4. Load to PostgreSQL
    load_to_postgres(df, engine)

    # 5. Verify
    verify_load(engine, DB_SCHEMA, TABLE_NAME)

    print("\n── Load Summary ────────────────────────────────────────────")
    print(f"Table:    {DB_SCHEMA}.{TABLE_NAME}")
    print(f"Records:  {len(df)}")
    print(f"Columns:  {list(df.columns)}")
    print(f"\nNext step: open DBeaver and run SQL analysis queries.")
