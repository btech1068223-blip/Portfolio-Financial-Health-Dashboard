-- Database Schema for Portfolio Company Financial Health Dashboard

-- Drop existing views and tables if they exist
DROP VIEW IF EXISTS quarterly_summary;
DROP VIEW IF EXISTS annual_summary;
DROP TRIGGER IF EXISTS update_financials_timestamp;
DROP TABLE IF EXISTS financials;
DROP TABLE IF EXISTS companies;

-- Companies dimension table
CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL
);

-- Financials fact table
CREATE TABLE financials (
    financial_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    period_type TEXT CHECK(period_type IN ('quarterly', 'annual')) NOT NULL,
    date TEXT NOT NULL, -- Standardized YYYY-MM-DD
    metric TEXT NOT NULL, -- revenue, net_income, operating_cash_flow, total_debt, gross_margin
    value REAL NOT NULL,
    last_refreshed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    UNIQUE(company_id, period_type, date, metric)
);

-- Trigger to update last_refreshed on updates
CREATE TRIGGER update_financials_timestamp AFTER UPDATE ON financials
BEGIN
    UPDATE financials SET last_refreshed = CURRENT_TIMESTAMP WHERE financial_id = OLD.financial_id;
END;

-- Pivoted Quarterly Summary View
CREATE VIEW quarterly_summary AS
SELECT 
    c.ticker,
    c.company_name,
    f.date,
    MAX(CASE WHEN f.metric = 'revenue' THEN f.value END) AS revenue,
    MAX(CASE WHEN f.metric = 'net_income' THEN f.value END) AS net_income,
    MAX(CASE WHEN f.metric = 'operating_cash_flow' THEN f.value END) AS operating_cash_flow,
    MAX(CASE WHEN f.metric = 'total_debt' THEN f.value END) AS total_debt,
    MAX(CASE WHEN f.metric = 'gross_margin' THEN f.value END) AS gross_margin
FROM financials f
JOIN companies c ON f.company_id = c.company_id
WHERE f.period_type = 'quarterly'
GROUP BY c.ticker, f.date;

-- Pivoted Annual Summary View
CREATE VIEW annual_summary AS
SELECT 
    c.ticker,
    c.company_name,
    f.date,
    MAX(CASE WHEN f.metric = 'revenue' THEN f.value END) AS revenue,
    MAX(CASE WHEN f.metric = 'net_income' THEN f.value END) AS net_income,
    MAX(CASE WHEN f.metric = 'operating_cash_flow' THEN f.value END) AS operating_cash_flow,
    MAX(CASE WHEN f.metric = 'total_debt' THEN f.value END) AS total_debt,
    MAX(CASE WHEN f.metric = 'gross_margin' THEN f.value END) AS gross_margin
FROM financials f
JOIN companies c ON f.company_id = c.company_id
WHERE f.period_type = 'annual'
GROUP BY c.ticker, f.date;
