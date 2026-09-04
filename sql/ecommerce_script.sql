SELECT 'dim_date' AS tabla, COUNT(*) AS filas FROM dim_date
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_region', COUNT(*) FROM dim_region
UNION ALL
SELECT 'dim_payment_method', COUNT(*) FROM dim_payment_method
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales;