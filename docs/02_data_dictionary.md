# 2. Data and Schema

## 2.1 Raw files (data/raw)
- **customers.csv**: customer_id, signup_date, city, gender, age
- **products.csv**: product_id, product_name, category, unit_price (60 products, 6 categories)
- **orders.csv**: order_id, customer_id, order_date, payment_method (UPI, Card, COD, NetBanking, Wallet), status (Delivered, Cancelled, Returned)
- **order_items.csv**: order_id, product_id, quantity, discount_pct

## 2.2 Injected data problems (to show real cleaning skill)
- Duplicate orders, null payment methods, negative quantities, impossible ages (150), messy city text ("pune ")

## 2.3 Warehouse (data/processed/warehouse.db)
- Star schema: **fact_sales** (grain = one order line) joined to **dim_customer** and **dim_product**
- Grain matters: one row per order item, so count orders with `COUNT(DISTINCT order_id)` to avoid double counting
- Indexes on customer_id, order_date, category for fast filtering and grouping

## 2.4 Cleaning rules (etl.py)
- Drop duplicate order_id; fill null payment with "Unknown" (keep the row, the order is real)
- Remove quantity <= 0; fix ages outside 16-90 with the median; standardise city text (strip, title case); fill gender with "Unknown"
- Every rule counts affected rows into `reports/data_quality.json` (auditability)
