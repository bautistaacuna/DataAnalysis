-- ============================================================
-- GENERAL SALES
-- ============================================================

-- How much did the company sell per year, quarter and month?
SELECT
    d.calendar_year                        AS year,
    d.calendar_quarter                     AS quarter,
    d.month_number_of_year                 AS month_number,
    d.english_month_name                   AS month_name,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS total_sales,
    COUNT(DISTINCT f.sales_order_number)   AS total_orders
FROM dw.fact_internet_sales f
JOIN dw.dim_date d ON f.order_date_key = d.date_key
GROUP BY
    d.calendar_year,
    d.calendar_quarter,
    d.month_number_of_year,
    d.english_month_name
ORDER BY
    d.calendar_year,
    d.calendar_quarter,
    d.month_number_of_year;

-- Which months had the highest and lowest sales volume?
SELECT
    d.calendar_year                        AS year,
    d.english_month_name                   AS month_name,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS total_sales,
    COUNT(DISTINCT f.sales_order_number)   AS total_orders,
    RANK() OVER (ORDER BY SUM(f.sales_amount) DESC) AS sales_rank
FROM dw.fact_internet_sales f
JOIN dw.dim_date d ON f.order_date_key = d.date_key
GROUP BY
    d.calendar_year,
    d.month_number_of_year,
    d.english_month_name
ORDER BY
    total_sales DESC;

-- How did sales evolve over time?
SELECT
    d.calendar_year                             AS year,
    d.month_number_of_year                      AS month_number,
    d.english_month_name                        AS month_name,
    ROUND(SUM(f.sales_amount)::numeric, 2)      AS total_sales,
    ROUND(LAG   (SUM(f.sales_amount)) OVER (
        ORDER BY d.calendar_year, d.month_number_of_year
    )::numeric, 2)                              AS prev_month_sales,
    ROUND((SUM(f.sales_amount) - LAG(SUM(f.sales_amount)) OVER (
        ORDER BY d.calendar_year, d.month_number_of_year
    )) / NULLIF(LAG(SUM(f.sales_amount)) OVER (
        ORDER BY d.calendar_year, d.month_number_of_year
    ), 0) * 100, 2)                             AS growth_pct
FROM dw.fact_internet_sales f
JOIN dw.dim_date d ON f.order_date_key = d.date_key
GROUP BY
    d.calendar_year,
    d.month_number_of_year,
    d.english_month_name
ORDER BY
    d.calendar_year,
    d.month_number_of_year;

-- ============================================================
-- PRODUCTS
-- ============================================================

-- Which product categories and subcategories generate the most revenue?
SELECT
    pc.english_product_category_name        AS category,
    ps.english_product_subcategory_name     AS subcategory,
    ROUND(SUM(f.sales_amount)::numeric, 2)  AS total_sales,
    ROUND(SUM(f.order_quantity)::numeric, 0) AS total_units,
    COUNT(DISTINCT f.sales_order_number)    AS total_orders,
    ROUND(SUM(f.sales_amount)::numeric / NULLIF(SUM(f.order_quantity), 0), 2) AS avg_price
FROM dw.fact_internet_sales f
JOIN dw.dim_product p           ON f.product_key = p.product_key
JOIN dw.dim_product_subcategory ps ON p.product_subcategory_key = ps.product_subcategory_key
JOIN dw.dim_product_category pc ON ps.product_category_key = pc.product_category_key
GROUP BY
    pc.english_product_category_name,
    ps.english_product_subcategory_name
ORDER BY
    total_sales DESC;

-- Which products have the highest and lowest profit margin?
SELECT
    p.english_product_name                              AS product,
    pc.english_product_category_name                    AS category,
    ROUND(p.list_price::numeric, 2)                     AS list_price,
    ROUND(p.standard_cost::numeric, 2)                  AS standard_cost,
    ROUND((p.list_price - p.standard_cost)::numeric, 2) AS margin,
    ROUND(((p.list_price - p.standard_cost) / 
        NULLIF(p.list_price, 0) * 100)::numeric, 2)     AS margin_pct,
    RANK() OVER (ORDER BY 
        (p.list_price - p.standard_cost) / 
        NULLIF(p.list_price, 0) DESC)                   AS margin_rank
FROM dw.dim_product p
JOIN dw.dim_product_subcategory ps ON p.product_subcategory_key = ps.product_subcategory_key
JOIN dw.dim_product_category pc    ON ps.product_category_key = pc.product_category_key
WHERE p.list_price > 0
ORDER BY margin_pct DESC;

-- ============================================================
-- RESELLERS
-- ============================================================

-- Which resellers generate the most revenue?
SELECT
    r.reseller_name                                 AS reseller,
    r.business_type                                 AS business_type,
    g.english_country_region_name                   AS country,
    g.state_province_name                           AS state,
    ROUND(SUM(f.sales_amount)::numeric, 2)          AS total_sales,
    COUNT(DISTINCT f.sales_order_number)            AS total_orders,
    ROUND(AVG(f.sales_amount)::numeric, 2)          AS avg_order_value,
    RANK() OVER (ORDER BY SUM(f.sales_amount) DESC) AS sales_rank
FROM dw.fact_reseller_sales f
JOIN dw.dim_reseller r      ON f.reseller_key = r.reseller_key
JOIN dw.dim_geography g     ON r.geography_key = g.geography_key
GROUP BY
    r.reseller_name,
    r.business_type,
    g.english_country_region_name,
    g.state_province_name
ORDER BY
    total_sales DESC
LIMIT 20;

-- Which resellers stopped buying?
SELECT
    r.reseller_name                             AS reseller,
    g.english_country_region_name               AS country,
    MIN(d.calendar_year)                        AS first_purchase_year,
    MAX(d.calendar_year)                        AS last_purchase_year,
    COUNT(DISTINCT f.sales_order_number)        AS total_orders,
    ROUND(SUM(f.sales_amount)::numeric, 2)      AS total_sales
FROM dw.fact_reseller_sales f
JOIN dw.dim_reseller r  ON f.reseller_key = r.reseller_key
JOIN dw.dim_geography g ON r.geography_key = g.geography_key
JOIN dw.dim_date d      ON f.order_date_key = d.date_key
GROUP BY
    r.reseller_name,
    g.english_country_region_name
HAVING
    MAX(d.calendar_year) < 2013
ORDER BY
    last_purchase_year DESC,
    total_sales DESC;

-- ============================================================
-- SALESPEOPLE
-- ============================================================

-- Which salespeople generate the most revenue?
SELECT
    e.first_name || ' ' || e.last_name              AS salesperson,
    st.sales_territory_country                      AS country,
    ROUND(SUM(f.sales_amount)::numeric, 2)          AS total_sales,
    COUNT(DISTINCT f.sales_order_number)            AS total_orders,
    ROUND(AVG(f.sales_amount)::numeric, 2)          AS avg_order_value,
    RANK() OVER (ORDER BY SUM(f.sales_amount) DESC) AS sales_rank
FROM dw.fact_reseller_sales f
JOIN dw.dim_employee e          ON f.employee_key = e.employee_key
JOIN dw.dim_sales_territory st  ON f.sales_territory_key = st.sales_territory_key
WHERE e.sales_person_flag = 1
GROUP BY
    e.first_name,
    e.last_name,
    st.sales_territory_country
ORDER BY
    total_sales DESC;

-- Which salespeople meet their quota and which don't?
WITH actual_sales AS (
    SELECT
        f.employee_key,
        d.calendar_year,
        d.calendar_quarter,
        ROUND(SUM(f.sales_amount)::numeric, 2) AS actual_sales
    FROM dw.fact_reseller_sales f
    JOIN dw.dim_date d ON f.order_date_key = d.date_key
    GROUP BY
        f.employee_key,
        d.calendar_year,
        d.calendar_quarter
),
quotas AS (
    SELECT
        q.employee_key,
        q.calendar_year,
        q.calendar_quarter,
        ROUND(q.sales_amount_quota::numeric, 2) AS quota
    FROM dw.fact_sales_quota q
)

SELECT
    e.first_name || ' ' || e.last_name          AS salesperson,
    a.calendar_year                             AS year,
    a.calendar_quarter                          AS quarter,
    a.actual_sales,
    q.quota,
    ROUND((a.actual_sales - q.quota)::numeric, 2)              AS difference,
    ROUND((a.actual_sales / NULLIF(q.quota, 0) * 100)::numeric, 2) AS pct_of_quota,
    CASE
        WHEN a.actual_sales >= q.quota THEN 'Met'
        ELSE 'Missed'
    END                                         AS quota_status
FROM actual_sales a 
JOIN quotas q       ON a.employee_key = q.employee_key
                   AND a.calendar_year = q.calendar_year
                   AND a.calendar_quarter = q.calendar_quarter
JOIN dw.dim_employee e ON a.employee_key = e.employee_key
WHERE e.sales_person_flag = 1
ORDER BY
    a.calendar_year,
    a.calendar_quarter,
    pct_of_quota DESC;