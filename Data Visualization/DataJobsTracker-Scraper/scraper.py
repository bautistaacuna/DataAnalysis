"""
Data Jobs Market Tracker — Stage 1: Scraper
Source: We Work Remotely (public RSS category feeds)
Strategy: fetch multiple category feeds + general feed,
          filter data-related roles by title and skills.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

# WWR public RSS feeds by category — each returns up to 100 listings.
# These are confirmed working (no search endpoint needed).
RSS_FEEDS = [
    "https://weworkremotely.com/remote-jobs.rss",
    "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-management-jobs.rss",
    "https://weworkremotely.com/categories/remote-all-other-jobs.rss",
]

# Keywords matched ONLY against job title and skills tags (not description).
# Specific phrases to avoid false positives from generic tech roles.
DATA_KEYWORDS = [
    "data analyst",
    "data engineer",
    "data scientist",
    "data science",
    "business intelligence",
    "bi analyst",
    "bi engineer",
    "analytics engineer",
    "machine learning",
    "ml engineer",
    "etl",
    "tableau",
    "power bi",
    "looker",
    "dbt",
    "snowflake",
    "data warehouse",
    "data pipeline",
    "airflow",
    "spark",
]

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Scraping functions ─────────────────────────────────────────────────────────

def fetch_feed(url: str) -> BeautifulSoup | None:
    """Downloads an RSS feed and returns a BeautifulSoup object."""
    try:
        delay = random.uniform(2, 4)
        log.info(f"  Waiting {delay:.1f}s...")
        time.sleep(delay)

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")
        log.info(f"  Feed downloaded OK")
        return soup

    except requests.exceptions.HTTPError as e:
        log.error(f"  HTTP {e.response.status_code} — {url}")
        return None
    except requests.exceptions.Timeout:
        log.error(f"  Timeout — {url}")
        return None
    except requests.exceptions.RequestException as e:
        log.error(f"  Connection error: {e}")
        return None


def extract_job_data(item: BeautifulSoup) -> dict | None:
    """
    Extracts fields from a single RSS <item>.

    WWR RSS structure:
        <title>     CompanyName: Job Title           </title>
        <region>    Anywhere in the World            </region>
        <category>  Data and Analytics               </category>
        <type>      Full-Time                        </type>
        <skills>    SQL, Python, Tableau, ...        </skills>
        <pubDate>   Thu, 18 Jun 2026 02:19:12 +0000  </pubDate>
        <guid>      https://weworkremotely.com/...   </guid>
        <description> HTML content in CDATA          </description>
    """
    try:
        # Title: "CompanyName: Job Title" — split on first colon
        raw_title = item.find("title")
        raw_title = raw_title.get_text(strip=True) if raw_title else ""

        if ":" in raw_title:
            parts   = raw_title.split(":", 1)
            company = parts[0].strip()
            title   = parts[1].strip()
        else:
            company = "N/A"
            title   = raw_title

        if not title:
            return None

        guid_tag = item.find("guid")
        url = guid_tag.get_text(strip=True) if guid_tag else None

        region_tag = item.find("region")
        region = region_tag.get_text(strip=True) if region_tag else "Anywhere"

        category_tag = item.find("category")
        category = category_tag.get_text(strip=True) if category_tag else "N/A"

        type_tag = item.find("type")
        job_type = type_tag.get_text(strip=True) if type_tag else None

        skills_tag = item.find("skills")
        skills = skills_tag.get_text(strip=True) if skills_tag else None

        date_tag = item.find("pubDate")
        published_date = date_tag.get_text(strip=True) if date_tag else None

        desc_tag = item.find("description")
        description_snippet = None
        if desc_tag:
            desc_html  = desc_tag.get_text()
            desc_soup  = BeautifulSoup(desc_html, "html.parser")
            plain_text = desc_soup.get_text(separator=" ", strip=True)
            description_snippet = plain_text[:500]

        return {
            "title":          title,
            "company":        company,
            "region":         region,
            "job_type":       job_type,
            "category":       category,
            "skills":         skills,
            "description":    description_snippet,
            "published_date": published_date,
            "url":            url,
            "scraped_at":     datetime.now().isoformat(),
        }

    except Exception as e:
        log.warning(f"  Error extracting item: {e}")
        return None


def is_data_related(title: str, skills: str | None) -> bool:
    """
    Returns True if the role is data-related.
    Checks ONLY title and skills — not description — to avoid false positives.
    """
    text = " ".join([title or "", skills or ""]).lower()
    return any(keyword in text for keyword in DATA_KEYWORDS)


def parse_feed(soup: BeautifulSoup) -> list[dict]:
    """Parses all <item> elements and filters data-related roles."""
    items = soup.find_all("item")
    if not items:
        log.warning("  No <item> elements found.")
        return []

    log.info(f"  {len(items)} total listings in feed")

    jobs = []
    for item in items:
        job = extract_job_data(item)
        if job and is_data_related(job["title"], job.get("skills")):
            jobs.append(job)

    log.info(f"  {len(jobs)} data-related listings kept")
    return jobs


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate listings by URL.
    Same job can appear in multiple category feeds.
    """
    initial = len(df)
    df = df.dropna(subset=["title"])
    df = df.drop_duplicates(subset=["url"], keep="first")
    removed = initial - len(df)
    log.info(f"Deduplication: {removed} duplicates removed → {len(df)} unique records")
    return df


def save_raw(df: pd.DataFrame) -> Path:
    """Saves the raw CSV with a timestamp in the filename."""
    ts          = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = OUTPUT_DIR / f"jobs_raw_{ts}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    log.info(f"CSV saved at: {output_path}")
    return output_path


# ── Main pipeline ──────────────────────────────────────────────────────────────

def scrape_all_feeds() -> pd.DataFrame:
    """Iterates over all RSS feeds and returns a combined DataFrame."""
    all_jobs = []

    for url in RSS_FEEDS:
        log.info(f"\n── Feed: {url.split('/')[-1]} ──────────────────────────────")
        log.info(f"  URL: {url}")

        soup = fetch_feed(url)
        if not soup:
            continue

        jobs = parse_feed(soup)
        all_jobs.extend(jobs)
        log.info(f"  Running total (before dedup): {len(all_jobs)}")

    if not all_jobs:
        log.error("No data obtained from any feed.")
        return pd.DataFrame()

    df = pd.DataFrame(all_jobs)
    log.info(f"\nTotal raw records (before dedup): {len(df)}")
    return df


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Data Jobs Market Tracker — Stage 1: Scraper")

    df_raw   = scrape_all_feeds()

    if df_raw.empty:
        log.error("Pipeline finished with no data.")
    else:
        df_clean    = deduplicate(df_raw)
        output_path = save_raw(df_clean)

        print("\n── All titles found ────────────────────────────────────")
        for i, row in df_clean.iterrows():
            print(f"  {i+1:02d}. {row['title']} — {row['company']}")

        print(f"\nColumns:       {list(df_clean.columns)}")
        print(f"Total records: {len(df_clean)}")
        print(f"File saved at: {output_path}")
