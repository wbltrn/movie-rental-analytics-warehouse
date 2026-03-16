
USE movie_rental_dw;

-- 1. Total Revenue
SELECT
    SUM(payment_amount) AS total_revenue
FROM fact_rental_payment;


-- 2. Revenue by Store
SELECT
    s.store_id,
    s.city,
    s.country,
    SUM(f.payment_amount) AS revenue
FROM fact_rental_payment f
JOIN dim_store s
ON f.store_key = s.store_key
GROUP BY s.store_id, s.city, s.country
ORDER BY revenue DESC;


-- 3. Top 10 Films by Revenue
SELECT
    f.title,
    SUM(fp.payment_amount) AS revenue
FROM fact_rental_payment fp
JOIN dim_film f
ON fp.film_key = f.film_key
GROUP BY f.title
ORDER BY revenue DESC
LIMIT 10;


-- 4. Late Rentals by Country
SELECT
    c.country,
    COUNT(*) AS late_rentals,
    AVG(days_late) AS avg_days_late
FROM fact_rental_payment f
JOIN dim_customer c
ON f.customer_key = c.customer_key
WHERE is_late = 1
GROUP BY c.country
ORDER BY late_rentals DESC;