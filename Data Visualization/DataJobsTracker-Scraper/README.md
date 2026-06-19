# Data Jobs Tracker — Scraper

Web scraper that collects remote data-related job listings from **We Work Remotely** using its public RSS/XML feeds. Part of a two-project series demonstrating two different data-collection techniques: web scraping (this repo) and REST API consumption ([DataJobsTracker-API](../DataJobsTracker-API)).

## What it does

- Fetches the WWR public RSS feed (`weworkremotely.com/remote-jobs.rss`)
- Parses XML structure with BeautifulSoup to extract job listings
- Splits company name and job title from the combined RSS `<title>` field
- Extracts region, category, job type, skills, and description per listing
- Filters results to data-related roles using a title/skills keyword match (avoids false positives from generic tech roles whose descriptions happen to mention "SQL" or "Python")
- Deduplicates by listing URL
- Saves a timestamped CSV to `data/raw/`

## Tech stack

| Tool | Purpose |
|---|---|
| `requests` | HTTP requests to the RSS feed |
| `BeautifulSoup` (lxml parser) | XML/RSS parsing |
| `pandas` | Deduplication and CSV export |

## Known limitations

This was a deliberate exploration of scraping constraints on a real public site:

- **WWR's search endpoint (`/remote-jobs/search.rss?term=`) returns HTTP 406** when accessed programmatically — it actively blocks non-browser requests, unlike the general feed.
- **Category-specific feeds are inconsistent** — some (e.g. `remote-data-science-jobs.rss`) return empty results even though the category page shows listings on the website.
- **Low volume of true "data" roles** in the general feed at any given time (WWR is a broad remote-jobs board, not data-specialized), resulting in a small but precise dataset after filtering.

These constraints are why the companion project, [DataJobsTracker-API](../DataJobsTracker-API), uses the Adzuna API instead — to obtain higher volume, richer fields (salary, location, contract type) and broader country coverage.

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python scraper.py
```

Output: `data/raw/jobs_raw_<timestamp>.csv`

## Author

Juan Bautista Acuña — [GitHub](https://github.com/bautistaacuna) · [Portfolio](https://bautistaacuna.github.io/DataAnalysis/)
