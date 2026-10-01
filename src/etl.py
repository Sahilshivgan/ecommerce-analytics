"""Step 2 - Clean raw files, build a star schema in SQLite, log data quality."""
import numpy as np, pandas as pd, json
from utils import RAW, DB, ROOT, conn

q = {}
cust, prod = pd.read_csv(RAW / "customers.csv"), pd.read_csv(RAW / "products.csv")
orders, items = pd.read_csv(RAW / "orders.csv"), pd.read_csv(RAW / "order_items.csv")

q["raw_orders"] = len(orders)
orders = orders.drop_duplicates("order_id")
q["duplicate_orders_removed"] = q["raw_orders"] - len(orders)
q["null_payment_filled"] = int(orders.payment_method.isna().sum())
orders["payment_method"] = orders.payment_method.fillna("Unknown")
orders["order_date"] = pd.to_datetime(orders.order_date, errors="coerce")
q["bad_dates_dropped"] = int(orders.order_date.isna().sum())
orders = orders.dropna(subset=["order_date"])

q["raw_items"] = len(items)
items = items[items.quantity > 0]
q["invalid_quantity_removed"] = q["raw_items"] - len(items)

cust["city"] = cust.city.str.strip().str.title()
bad_age = ~cust.age.between(16, 90)
q["age_outliers_fixed"] = int(bad_age.sum())
cust.loc[bad_age, "age"] = int(cust.loc[~bad_age, "age"].median())
cust["gender"] = cust.gender.fillna("Unknown")

fact = items.merge(prod, on="product_id").merge(orders, on="order_id")
fact["revenue"] = (fact.quantity * fact.unit_price * (1 - fact.discount_pct / 100)).round(2)
fact["order_date"] = fact.order_date.dt.strftime("%Y-%m-%d")
fact = fact[["order_id", "customer_id", "product_id", "category", "order_date", "status",
             "payment_method", "quantity", "unit_price", "discount_pct", "revenue"]]
q["fact_rows"] = len(fact)

c = conn()
cust.to_sql("dim_customer", c, if_exists="replace", index=False)
prod.to_sql("dim_product", c, if_exists="replace", index=False)
fact.to_sql("fact_sales", c, if_exists="replace", index=False)
for ix in ("customer_id", "order_date", "category"):
    c.execute(f"CREATE INDEX IF NOT EXISTS ix_{ix} ON fact_sales({ix})")
c.commit(); c.close()
(ROOT / "reports/data_quality.json").write_text(json.dumps(q, indent=2))
print(q)
