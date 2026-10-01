"""Step 1 - Simulate a realistic, deliberately messy e-commerce dataset (India)."""
import numpy as np, pandas as pd
from utils import RAW

rng = np.random.default_rng(42)
N_C = 5000
cities = ["Pune", "Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad"]
signup = pd.Timestamp("2023-01-01") + pd.to_timedelta(rng.integers(0, 540, N_C), unit="D")
cust = pd.DataFrame({
    "customer_id": np.arange(1, N_C + 1), "signup_date": signup.date,
    "city": rng.choice(cities, N_C, p=[.12, .2, .18, .18, .1, .07, .1, .05]),
    "gender": rng.choice(["M", "F", None], N_C, p=[.48, .48, .04]),
    "age": rng.integers(18, 65, N_C)})

cats = {"Electronics": (800, 25000), "Fashion": (300, 4000), "Home": (250, 8000),
        "Beauty": (150, 2500), "Grocery": (50, 1200), "Sports": (400, 9000)}
prods, pid = [], 1
for c, (lo, hi) in cats.items():
    for _ in range(10):
        prods.append((pid, f"{c}-{pid}", c, round(float(rng.uniform(lo, hi)), 2))); pid += 1
prod = pd.DataFrame(prods, columns=["product_id", "product_name", "category", "unit_price"])

days = pd.date_range("2023-01-01", "2024-12-31")
mf = {1: .8, 2: .8, 3: .9, 4: .9, 5: 1, 6: .9, 7: .9, 8: 1, 9: 1.1, 10: 1.5, 11: 1.6, 12: 1.3}  # festive season
w_all = np.array([mf[d.month] for d in days])
rows, oid = [], 1
for cid, sd in zip(cust.customer_id, pd.to_datetime(cust.signup_date)):
    n = rng.poisson(rng.gamma(2, 2))
    m = days >= sd
    if n == 0 or m.sum() == 0:
        continue
    w = w_all[m] / w_all[m].sum()
    for dt in rng.choice(days[m], n, p=w):
        rows.append((oid, cid, pd.Timestamp(dt).date())); oid += 1
orders = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date"])
orders["payment_method"] = rng.choice(["UPI", "Card", "COD", "NetBanking", "Wallet"], len(orders), p=[.4, .25, .2, .1, .05])
orders["status"] = rng.choice(["Delivered", "Cancelled", "Returned"], len(orders), p=[.9, .04, .06])

k = rng.integers(1, 5, len(orders))
items = orders[["order_id"]].loc[orders.index.repeat(k)].reset_index(drop=True)
pop = 1 / np.arange(1, 61) ** 0.5; pop /= pop.sum()
items["product_id"] = rng.choice(prod.product_id, len(items), p=pop)
items["quantity"] = rng.choice([1, 2, 3], len(items), p=[.7, .2, .1])
items["discount_pct"] = rng.choice([0, 5, 10, 20], len(items), p=[.4, .2, .25, .15])

# --- inject real-world dirt ---
orders = pd.concat([orders, orders.sample(frac=.01, random_state=1)])                 # duplicates
orders.loc[orders.sample(frac=.02, random_state=2).index, "payment_method"] = None     # nulls
items.loc[items.sample(frac=.003, random_state=3).index, "quantity"] = -1              # bad qty
cust.loc[cust.sample(frac=.01, random_state=4).index, "age"] = 150                     # outliers
idx = cust.sample(frac=.04, random_state=5).index
cust.loc[idx, "city"] = cust.loc[idx, "city"].str.lower() + " "                        # messy text

cust.to_csv(RAW / "customers.csv", index=False)
prod.to_csv(RAW / "products.csv", index=False)
orders.to_csv(RAW / "orders.csv", index=False)
items.to_csv(RAW / "order_items.csv", index=False)
print(f"customers={len(cust)} orders={len(orders)} items={len(items)}")
