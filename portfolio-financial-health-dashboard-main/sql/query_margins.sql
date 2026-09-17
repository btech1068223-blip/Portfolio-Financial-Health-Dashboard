-- 4-Quarter Rolling Average Margins (Gross Margin and Operating Cash Flow Margin)
WITH margins_calc AS (
    SELECT 
        ticker,
        company_name,
        date,
        gross_margin,
        CASE 
            WHEN revenue IS NOT NULL AND revenue > 0 AND operating_cash_flow IS NOT NULL 
            THEN operating_cash_flow / revenue 
            ELSE NULL 
        END AS ocf_margin
    FROM quarterly_summary
)
SELECT 
    ticker,
    company_name,
    date,
    gross_margin,
    AVG(gross_margin) OVER (
        PARTITION BY ticker 
        ORDER BY date 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS gross_margin_4q_rolling,
    ocf_margin,
    AVG(ocf_margin) OVER (
        PARTITION BY ticker 
        ORDER BY date 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS ocf_margin_4q_rolling
FROM margins_calc
ORDER BY ticker, date DESC;
