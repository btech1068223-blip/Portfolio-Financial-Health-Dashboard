-- Identify companies with 2 or more consecutive quarters of decelerating QoQ revenue growth
WITH quarterly_qoq AS (
    SELECT 
        ticker,
        company_name,
        date,
        revenue,
        LAG(revenue, 1) OVER (PARTITION BY ticker ORDER BY date) AS prev_revenue
    FROM quarterly_summary
),
growth_calc AS (
    SELECT 
        ticker,
        company_name,
        date,
        CASE 
            WHEN prev_revenue IS NOT NULL AND prev_revenue > 0 
            THEN (revenue - prev_revenue) / prev_revenue 
            ELSE NULL 
        END AS revenue_qoq_growth
    FROM quarterly_qoq
),
growth_diffs AS (
    SELECT 
        ticker,
        company_name,
        date,
        revenue_qoq_growth,
        LAG(revenue_qoq_growth, 1) OVER (PARTITION BY ticker ORDER BY date) AS prev_growth,
        LAG(revenue_qoq_growth, 2) OVER (PARTITION BY ticker ORDER BY date) AS prev_prev_growth
    FROM growth_calc
)
SELECT 
    ticker,
    company_name,
    date,
    revenue_qoq_growth,
    prev_growth,
    prev_prev_growth
FROM growth_diffs
WHERE revenue_qoq_growth IS NOT NULL 
  AND prev_growth IS NOT NULL 
  AND prev_prev_growth IS NOT NULL
  AND revenue_qoq_growth < prev_growth
  AND prev_growth < prev_prev_growth
ORDER BY ticker, date DESC;
