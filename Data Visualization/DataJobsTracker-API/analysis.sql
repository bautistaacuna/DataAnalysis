-- ============================================================
-- Data Jobs Market Tracker — Stage 4: SQL Analysis
-- Table: dw.data_jobs_market
-- ============================================================


-- ── 1. Market overview ──────────────────────────────────────
-- How many jobs are there per country and what percentage
-- of the total does each represent?

select
    country,
    COUNT(*)                                                AS total_jobs,
    COUNT(*) FILTER (WHERE is_remote = true)                AS remote_jobs,
    COUNT(*) FILTER (WHERE salary_avg IS NOT NULL)          AS jobs_with_salary,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2)     AS pct_of_total
FROM dw.data_jobs_market
GROUP BY country
ORDER BY total_jobs DESC;


-- ── 2. Top job titles by demand ─────────────────────────────
-- Which data roles are most in demand across all markets?

SELECT
    title,
    COUNT(*)                                                AS total_postings,
    COUNT(DISTINCT country)                                 AS countries_present,
    ROUND(AVG(CASE WHEN salary_avg IS NOT NULL
               THEN salary_avg END)::NUMERIC, 2)            AS avg_salary
FROM dw.data_jobs_market
GROUP BY title
HAVING COUNT(*) >= 10
ORDER BY total_postings DESC
LIMIT 20;


-- ── 3. Salary analysis by role ──────────────────────────────
-- What is the salary range for each data role?
-- Uses CTE to aggregate by normalized title group.

WITH role_salaries AS (
    SELECT
        search_term                                         AS role,
        COUNT(*)                                            AS total_jobs,
        COUNT(*) FILTER (
            WHERE salary_avg IS NOT NULL)                   AS jobs_with_salary,
        ROUND(MIN(salary_avg)::NUMERIC, 0)                  AS salary_min,
        ROUND(MAX(salary_avg)::NUMERIC, 0)                  AS salary_max,
        ROUND(AVG(salary_avg)::NUMERIC, 0)                  AS salary_avg,
        ROUND(PERCENTILE_CONT(0.5)
            WITHIN GROUP (ORDER BY salary_avg)::NUMERIC, 0) AS salary_median
    FROM dw.data_jobs_market
    WHERE salary_avg IS NOT NULL
      AND salary_avg > 10000
    GROUP BY search_term
)
SELECT *
FROM role_salaries
ORDER BY salary_median DESC;


-- ── 4. Seniority distribution by country ────────────────────
-- How does seniority demand vary across countries?

SELECT
    country,
    seniority,
    COUNT(*)                                                AS total_jobs,
    ROUND(COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (PARTITION BY country), 1)      AS pct_in_country
FROM dw.data_jobs_market
GROUP BY country, seniority
ORDER BY country, total_jobs DESC;


-- ── 5. Salary ranking by country using Window Functions ─────
-- For each country, rank roles by average salary.
-- Demonstrates: Window Functions, RANK(), PARTITION BY

WITH country_role_salary AS (
    SELECT
        country,
        search_term                                         AS role,
        COUNT(*)                                            AS job_count,
        ROUND(AVG(salary_avg)::NUMERIC, 0)                  AS avg_salary
    FROM dw.data_jobs_market
    WHERE salary_avg IS NOT NULL
      AND salary_avg > 10000
    GROUP BY country, search_term
    HAVING COUNT(*) >= 3
),
ranked AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY country
            ORDER BY avg_salary DESC
        ) AS salary_rank
    FROM country_role_salary
)
SELECT *
FROM ranked
WHERE salary_rank <= 3
ORDER BY country, salary_rank;


-- ── 6. Remote job availability by role ──────────────────────
-- Which roles have the highest proportion of remote positions?

SELECT
    search_term                                             AS role,
    COUNT(*)                                                AS total_jobs,
    COUNT(*) FILTER (WHERE is_remote = true)                AS remote_jobs,
    ROUND(
        COUNT(*) FILTER (WHERE is_remote = true) * 100.0
        / NULLIF(COUNT(*), 0), 1
    )                                                       AS remote_pct
FROM dw.data_jobs_market
GROUP BY search_term
ORDER BY remote_pct DESC;


-- ── 7. Job posting trend by date ────────────────────────────
-- How many jobs were posted each day? Identifies hiring peaks.

SELECT
    published_date,
    COUNT(*)                                                AS jobs_posted,
    SUM(COUNT(*)) OVER (
        ORDER BY published_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                       AS cumulative_jobs
FROM dw.data_jobs_market
WHERE published_date IS NOT NULL
GROUP BY published_date
ORDER BY published_date DESC
LIMIT 30;


-- ── 8. Top hiring companies ─────────────────────────────────
-- Which companies are hiring the most data professionals?

SELECT
    company,
    COUNT(*)                                                AS total_postings,
    COUNT(DISTINCT search_term)                             AS roles_hiring_for,
    COUNT(DISTINCT country)                                 AS countries,
    ROUND(AVG(CASE WHEN salary_avg IS NOT NULL
               THEN salary_avg END)::NUMERIC, 0)            AS avg_salary_offered
FROM dw.data_jobs_market
WHERE company != 'N/A'
GROUP BY company
HAVING COUNT(*) >= 5
ORDER BY total_postings DESC
LIMIT 20;


-- ── 9. Salary percentiles by seniority ──────────────────────
-- What salary can you expect at each career level?

SELECT
    seniority,
    COUNT(*)                                                        AS jobs,
    ROUND(PERCENTILE_CONT(0.25)
        WITHIN GROUP (ORDER BY salary_avg)::NUMERIC, 0)            AS p25_salary,
    ROUND(PERCENTILE_CONT(0.50)
        WITHIN GROUP (ORDER BY salary_avg)::NUMERIC, 0)            AS median_salary,
    ROUND(PERCENTILE_CONT(0.75)
        WITHIN GROUP (ORDER BY salary_avg)::NUMERIC, 0)            AS p75_salary,
    ROUND(AVG(salary_avg)::NUMERIC, 0)                             AS mean_salary
FROM dw.data_jobs_market
WHERE salary_avg IS NOT NULL
  AND salary_avg > 10000
  AND seniority != 'Not specified'
GROUP BY seniority
ORDER BY median_salary DESC;


-- ── 10. Most valuable skill combinations ────────────────────
-- Distribution of roles by salary band using CASE WHEN.

WITH salary_bands AS (
    SELECT
        *,
        CASE
            WHEN salary_avg >= 120000 THEN 'High (120k+)'
            WHEN salary_avg >= 80000  THEN 'Mid (80k-120k)'
            WHEN salary_avg >= 40000  THEN 'Low (40k-80k)'
            ELSE 'Entry (<40k)'
        END AS salary_band
    FROM dw.data_jobs_market
    WHERE salary_avg IS NOT NULL
      AND salary_avg > 10000
)
SELECT
    search_term                 AS role,
    salary_band,
    COUNT(*)                    AS job_count
FROM salary_bands
GROUP BY search_term, salary_band
ORDER BY search_term, job_count DESC;
