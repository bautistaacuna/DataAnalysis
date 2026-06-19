"""
Data Jobs Market Tracker — Adzuna API Client
Source: Adzuna Job Search API (https://developer.adzuna.com)
Credentials: stored in .env file (never hardcoded)
"""

import requests
import pandas as pd
import time
import logging
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ── Load credentials from .env ─────────────────────────────────────────────────
load_dotenv()

APP_ID  = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# ── Configuration ──────────────────────────────────────────────────────────────

SEARCH_TERMS = [
    "data analyst",
    "data engineer",
    "data scientist",
    "business intelligence",
    "machine learning engineer",
    "analytics engineer",
    "etl developer",
    "bi developer",
]

# Countries selected based on:
# - Compatible timezone with Italy (CET/UTC+2)
# - Languages: English, Spanish, Portuguese
# - Active tech job markets on Adzuna
COUNTRIES = ["us", "gb", "nl", "de", "br", "es", "it"]

RESULTS_PER_PAGE = 50
MAX_PAGES        = 2

BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── API functions ──────────────────────────────────────────────────────────────

def fetch_jobs(term: str, country: str, page: int) -> list[dict]:
    """Fetches one page of remote job results from Adzuna API."""
    url = BASE_URL.format(country=country, page=page)

    params = {
        "app_id":           APP_ID,
        "app_key":          APP_KEY,
        "what":             term,
        "results_per_page": RESULTS_PER_PAGE,
    }

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()

        data    = response.json()
        results = data.get("results", [])
        total   = data.get("count", 0)

        log.info(f"  Page {page}: {len(results)} results (total available: {total})")
        return results

    except requests.exceptions.HTTPError as e:
        log.error(f"  HTTP {e.response.status_code} — {term} / {country} / page {page}")
        log.error(f"  Response: {e.response.text[:200]}")
        return []
    except requests.exceptions.Timeout:
        log.error(f"  Timeout — {term} / {country} / page {page}")
        return []
    except requests.exceptions.RequestException as e:
        log.error(f"  Connection error: {e}")
        return []


def parse_job(job: dict, term: str, country: str) -> dict:
    """Extracts and normalizes fields from a single Adzuna job result."""
    return {
        "job_id":         job.get("id"),
        "title":          job.get("title", "").strip(),
        "company":        job.get("company", {}).get("display_name", "N/A"),
        "location":       job.get("location", {}).get("display_name", "N/A"),
        "country":        country.upper(),
        "salary_min":     job.get("salary_min"),
        "salary_max":     job.get("salary_max"),
        "category":       job.get("category", {}).get("label", "N/A"),
        "contract_type":  job.get("contract_type"),
        "published_date": job.get("created"),
        "description":    job.get("description", "")[:500],
        "search_term":    term,
        "url":            job.get("redirect_url"),
        "scraped_at":     datetime.now().isoformat(),
    }


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate jobs by job_id."""
    initial = len(df)
    df = df.dropna(subset=["title"])
    df = df.drop_duplicates(subset=["job_id"], keep="first")
    removed = initial - len(df)
    log.info(f"Deduplication: {removed} duplicates removed → {len(df)} unique records")
    return df


def save_raw(df: pd.DataFrame) -> Path:
    """Saves the raw CSV with a timestamp in the filename."""
    ts          = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = OUTPUT_DIR / f"adzuna_raw_{ts}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    log.info(f"CSV saved at: {output_path}")
    return output_path


# ── Main pipeline ──────────────────────────────────────────────────────────────

def scrape_adzuna() -> pd.DataFrame:
    """Iterates over all search terms and countries and returns a combined DataFrame."""
    if not APP_ID or not APP_KEY:
        log.error("Missing credentials. Check your .env file.")
        return pd.DataFrame()

    all_jobs = []

    for term in SEARCH_TERMS:
        for country in COUNTRIES:
            log.info(f"\n── '{term}' / {country.upper()} ──────────────────────────────")

            for page in range(1, MAX_PAGES + 1):
                results = fetch_jobs(term, country, page)

                if not results:
                    break

                for job in results:
                    all_jobs.append(parse_job(job, term, country))

                time.sleep(1)

            time.sleep(2)

    if not all_jobs:
        log.error("No data obtained from Adzuna.")
        return pd.DataFrame()

    df = pd.DataFrame(all_jobs)
    log.info(f"\nTotal raw records (before dedup): {len(df)}")
    return df


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Data Jobs Market Tracker — Adzuna API")
    log.info(f"Search terms: {SEARCH_TERMS}")
    log.info(f"Countries:    {COUNTRIES}")
    log.info(f"Countries:    {COUNTRIES}")

    df_raw = scrape_adzuna()

    if df_raw.empty:
        log.error("Pipeline finished with no data.")
    else:
        df_clean    = deduplicate(df_raw)
        output_path = save_raw(df_clean)

        print("\n── Preview (first 10 rows) ─────────────────────────────")
        print(df_clean[["title", "company", "location", "country", "salary_min"]].head(10))
        print(f"\nRecords per country:")
        print(df_clean["country"].value_counts())
        print(f"\nTotal records: {len(df_clean)}")
        print(f"File saved at: {output_path}")
