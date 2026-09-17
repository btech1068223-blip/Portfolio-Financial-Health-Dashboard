-- Year-over-Year (YoY) growth for Revenue and Net Income per quarter
WITH quarterly_with_lag AS (
    SELECT 
        ticker,
        company_name,
        date,
        revenue,
        LAG(revenue, 4) OVER (PARTITION BY ticker ORDER BY date) AS prev_year_revenue,
        net_income,
        LAG(net_income, 4) OVER (PARTITION BY ticker ORDER BY date) AS prev_year_net_income
    FROM quarterly_summary
)
SELECT 
    ticker,
    company_name,
    date,
    revenue,
    prev_year_revenue,
    CASE 
        WHEN prev_year_revenue IS NOT NULL AND prev_year_revenue > 0 
        THEN (revenue - prev_year_revenue) / prev_year_revenue 
        ELSE NULL 
    END AS revenue_yoy_growth,
    net_income,
    prev_year_net_income,
    CASE 
        WHEN prev_year_net_income IS NOT NULL AND prev_year_net_income != 0 
        THEN (net_income - prev_year_net_income) / ABS(prev_year_net_income) 
        ELSE NULL 
    END AS net_income_yoy_growth
FROM quarterly_with_lag
ORDER BY ticker, date DESC;
