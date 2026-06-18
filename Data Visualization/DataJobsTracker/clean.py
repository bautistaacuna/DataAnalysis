"""
Data Jobs Market Tracker — Stage 2: Data Cleaning
Input:  data/raw/adzuna_raw_*.csv  (latest file)
Output: data/processed/jobs_clean_YYYYMMDD_HHMM.csv

Steps:
    1. Load latest raw CSV
    2. Drop nulls and duplicates
    3. Normalize text fields (title, company, location)
    4. Extract seniority level from title
    5. Filter remote jobs by description and location
    6. Clean salary columns
    7. Save processed CSV
"""

import pandas as pd
import re
import logging
from pathlib import Path
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────────

RAW_DIR       = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Helper functions ───────────────────────────────────────────────────────────

def load_latest_raw() -> pd.DataFrame:
    """Loads the most recent Adzuna raw CSV from data/raw/."""
    files = sorted(RAW_DIR.glob("adzuna_raw_*.csv"))

    if not files:
        raise FileNotFoundError("No raw CSV files found in data/raw/")

    latest = files[-1]
    log.info(f"Loading: {latest}")

    df = pd.read_csv(latest, encoding="utf-8-sig")
    log.info(f"Raw records loaded: {len(df)}")
    return df


def normalize_text(text: str) -> str:
    """
    Cleans a text field:
    - Strips leading/trailing whitespace
    - Removes extra internal spaces
    - Title case for readability
    """
    if not isinstance(text, str):
        return text
    text = text.strip()
    text = re.sub(r"\s+", " ", text)     # collapse multiple spaces
    return text


def extract_seniority(title: str) -> str:
    """
    Detects seniority level from the job title.
    Returns: 'Junior', 'Mid', 'Senior', or 'Not specified'
    """
    if not isinstance(title, str):
        return "Not specified"

    title_lower = title.lower()

    senior_keywords = ["senior", "sr.", "sr ", "lead", "principal", "staff", "head of", "manager"]
    junior_keywords = ["junior", "jr.", "jr ", "entry", "graduate", "intern", "trainee"]
    mid_keywords    = ["mid", "middle", "associate", "ii", "iii"]

    if any(kw in title_lower for kw in senior_keywords):
        return "Senior"
    if any(kw in title_lower for kw in junior_keywords):
        return "Junior"
    if any(kw in title_lower for kw in mid_keywords):
        return "Mid"
    return "Not specified"


def is_remote(location: str, description: str) -> bool:
    """
    Returns True if the job appears to be remote.
    Checks location field and description text.
    """
    remote_keywords = ["remote", "work from home", "wfh", "anywhere", "distributed"]

    location_text    = (location    or "").lower()
    description_text = (description or "").lower()

    return any(kw in location_text or kw in description_text for kw in remote_keywords)


def clean_salary(value) -> float | None:
    """
    Returns salary as float, or None if missing/invalid.
    Adzuna returns salaries as floats but some may be 0 or negative.
    """
    try:
        val = float(value)
        return val if val > 0 else None
    except (ValueError, TypeError):
        return None


def clean_date(date_str: str) -> str | None:
    """
    Normalizes Adzuna date format: '2026-06-18T12:00:00Z' → '2026-06-18'
    """
    if not isinstance(date_str, str):
        return None
    return date_str[:10]   # keep only YYYY-MM-DD


# ── Main cleaning pipeline ─────────────────────────────────────────────────────

def clean(df: pd.DataFrame) -> pd.DataFrame:
    log.info("\n── Step 1: Drop nulls and duplicates ──────────────────────")
    df = df.dropna(subset=["title", "job_id"])
    df = df.drop_duplicates(subset=["job_id"], keep="first")
    log.info(f"  Records after dedup: {len(df)}")

    log.info("\n── Step 2: Normalize text fields ──────────────────────────")
    df["title"]    = df["title"].apply(normalize_text)
    df["company"]  = df["company"].apply(normalize_text)
    df["location"] = df["location"].apply(normalize_text)
    log.info("  title, company, location normalized")

    log.info("\n── Step 3: Extract seniority ───────────────────────────────")
    df["seniority"] = df["title"].apply(extract_seniority)
    log.info(f"  Seniority distribution:\n{df['seniority'].value_counts().to_string()}")

    log.info("\n── Step 4: Filter remote jobs ──────────────────────────────")
    before = len(df)
    df["is_remote"] = df.apply(
        lambda row: is_remote(row.get("location", ""), row.get("description", "")),
        axis=1
    )
    remote_count = df["is_remote"].sum()
    log.info(f"  Remote jobs found: {remote_count} of {before}")

    log.info("\n── Step 5: Clean salary columns ────────────────────────────")
    df["salary_min"] = df["salary_min"].apply(clean_salary)
    df["salary_max"] = df["salary_max"].apply(clean_salary)
    df["salary_avg"] = df.apply(
        lambda row: (
            (row["salary_min"] + row["salary_max"]) / 2
            if pd.notna(row["salary_min"]) and pd.notna(row["salary_max"])
            else row["salary_min"] or row["salary_max"]
        ),
        axis=1
    )
    has_salary = df["salary_avg"].notna().sum()
    log.info(f"  Records with salary data: {has_salary} of {len(df)}")

    log.info("\n── Step 6: Normalize date ──────────────────────────────────")
    df["published_date"] = df["published_date"].apply(clean_date)

    log.info("\n── Step 7: Reorder columns ─────────────────────────────────")
    columns = [
        "job_id", "title", "seniority", "company", "location", "country",
        "is_remote", "salary_min", "salary_max", "salary_avg",
        "category", "contract_type", "published_date",
        "search_term", "description", "url", "scraped_at",
    ]
    # keep only columns that exist
    columns = [c for c in columns if c in df.columns]
    df = df[columns]

    return df


def save_processed(df: pd.DataFrame) -> Path:
    """Saves the clean CSV to data/processed/."""
    ts          = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = PROCESSED_DIR / f"jobs_clean_{ts}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    log.info(f"\nCSV saved at: {output_path}")
    return output_path


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Data Jobs Market Tracker — Stage 2: Cleaning")

    df_raw   = load_latest_raw()
    df_clean = clean(df_raw)
    path     = save_processed(df_clean)

    print("\n── Summary ─────────────────────────────────────────────────")
    print(f"Raw records:         {len(df_raw)}")
    print(f"Clean records:       {len(df_clean)}")
    print(f"Remote jobs:         {df_clean['is_remote'].sum()}")
    print(f"With salary data:    {df_clean['salary_avg'].notna().sum()}")
    print(f"\nSeniority breakdown:")
    print(df_clean["seniority"].value_counts().to_string())
    print(f"\nRecords per country:")
    print(df_clean["country"].value_counts().to_string())
    print(f"\nTop 10 titles:")
    print(df_clean["title"].value_counts().head(10).to_string())
    print(f"\nFile saved at: {path}")
