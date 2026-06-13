SELECT fund_house, aum_amount, date_id
FROM fact_aum
ORDER BY aum_amount DESC
LIMIT 5;

SELECT 
    n.amfi_code,
    d.year,
    d.month,
    AVG(n.nav) AS avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date_id = d.date_id
GROUP BY n.amfi_code, d.year, d.month
ORDER BY n.amfi_code, d.year, d.month;

SELECT 
    d.year,
    SUM(t.amount) AS total_sip_amount
FROM fact_transactions t
JOIN dim_date d ON t.date_id = d.date_id
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;

SELECT 
    state,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

SELECT amfi_code, expense_ratio
FROM fact_performance
WHERE expense_ratio < 1.0
ORDER BY expense_ratio ASC;

SELECT 
    investor_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_invested
FROM fact_transactions
WHERE transaction_type IN ('SIP', 'Lumpsum')
GROUP BY investor_id
ORDER BY total_invested DESC;

SELECT 
    amfi_code,
    SUM(CASE WHEN transaction_type IN ('SIP', 'Lumpsum') THEN amount ELSE 0 END) AS total_investment,
    SUM(CASE WHEN transaction_type = 'Redemption' THEN amount ELSE 0 END) AS total_redemption
FROM fact_transactions
GROUP BY amfi_code;

SELECT amfi_code, return_1y, return_3y, return_5y
FROM fact_performance
WHERE return_3y > 12.0
ORDER BY return_3y DESC;

SELECT 
    city_tier,
    COUNT(*) AS volume,
    SUM(amount) AS total_value
FROM fact_transactions
GROUP BY city_tier
ORDER BY city_tier;

SELECT 
    f.category,
    COUNT(t.investor_id) AS total_transactions_done
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY f.category
ORDER BY total_transactions_done DESC; 