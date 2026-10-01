-- name: monthly_revenue
SELECT strftime('%Y-%m', order_date) AS month, ROUND(SUM(revenue),0) AS revenue, COUNT(DISTINCT order_id) AS orders
FROM fact_sales WHERE status='Delivered' GROUP BY 1 ORDER BY 1;

-- name: status_mix
SELECT status, COUNT(DISTINCT order_id) AS orders FROM fact_sales GROUP BY status;

-- name: category_perf
SELECT category,
  ROUND(SUM(CASE WHEN status='Delivered' THEN revenue END),0) AS revenue,
  SUM(CASE WHEN status='Delivered' THEN quantity END) AS units,
  ROUND(AVG(discount_pct),1) AS avg_discount_pct,
  ROUND(100.0*SUM(status='Returned')/COUNT(*),1) AS return_rate_pct
FROM fact_sales GROUP BY category ORDER BY revenue DESC;

-- name: city_perf
SELECT c.city, ROUND(SUM(f.revenue),0) AS revenue, COUNT(DISTINCT f.order_id) AS orders, COUNT(DISTINCT f.customer_id) AS customers
FROM fact_sales f JOIN dim_customer c USING(customer_id)
WHERE f.status='Delivered' GROUP BY c.city ORDER BY revenue DESC;

-- name: payment_mix
SELECT payment_method, COUNT(DISTINCT order_id) AS orders, ROUND(100.0*SUM(status!='Delivered')/COUNT(*),1) AS failed_pct
FROM fact_sales GROUP BY payment_method ORDER BY orders DESC;

-- name: city_category_rank
SELECT city, category, revenue, RANK() OVER (PARTITION BY city ORDER BY revenue DESC) AS rnk
FROM (SELECT c.city, f.category, ROUND(SUM(f.revenue),0) AS revenue
      FROM fact_sales f JOIN dim_customer c USING(customer_id)
      WHERE f.status='Delivered' GROUP BY 1,2)
ORDER BY city, rnk;

-- name: rfm_base
SELECT customer_id, MAX(order_date) AS last_order, COUNT(DISTINCT order_id) AS frequency, ROUND(SUM(revenue),2) AS monetary
FROM fact_sales WHERE status='Delivered' GROUP BY customer_id;

-- name: cohort_base
SELECT DISTINCT customer_id, strftime('%Y-%m', order_date) AS order_month FROM fact_sales WHERE status='Delivered';

-- name: signups
SELECT strftime('%Y-%m', signup_date) AS month, COUNT(*) AS n FROM dim_customer GROUP BY 1;
