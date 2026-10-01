"""Step 4 - RFM customer segmentation."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils import *

d = query("rfm_base"); d["last_order"] = pd.to_datetime(d.last_order)
snap = d.last_order.max() + pd.Timedelta(days=1)
d["recency"] = (snap - d.last_order).dt.days
d["R"] = pd.qcut(d.recency.rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)   # recent = high score
d["F"] = d.frequency.clip(1, 5)                                                          # business-defined bins (ties!)
d["M"] = pd.qcut(d.monetary.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
d["segment"] = np.select(
    [(d.R >= 4) & (d.F >= 4), d.F >= 4, (d.R >= 4) & (d.F <= 2), (d.R <= 2) & (d.F >= 3), (d.R <= 2) & (d.F <= 2)],
    ["Champions", "Loyal", "New / Promising", "At Risk", "Lost"], default="Needs Attention")
s = d.groupby("segment").agg(customers=("customer_id", "count"), revenue=("monetary", "sum"), avg_value=("monetary", "mean")).round(0)
s["customer_pct"] = (100 * s.customers / s.customers.sum()).round(1); s["revenue_pct"] = (100 * s.revenue / s.revenue.sum()).round(1)
s = s.sort_values("revenue", ascending=False); s.to_csv(TAB / "rfm_segments.csv")
d.to_csv(PROC / "rfm_customers.csv", index=False)
ax = s.revenue_pct.plot.barh(figsize=(8, 4), color="#2a6f97"); ax.set_title("Revenue share by RFM segment (%)")
plt.tight_layout(); plt.savefig(FIG / "rfm_segments.png", dpi=130); plt.close()
g = lambda seg, col: float(s.loc[seg, col]) if seg in s.index else 0.0
save_metrics(active_customers=int(len(d)), champions_customer_pct=g("Champions", "customer_pct"), champions_revenue_pct=g("Champions", "revenue_pct"),
    at_risk_customers=int(g("At Risk", "customers")), at_risk_revenue_pct=g("At Risk", "revenue_pct"), lost_customer_pct=g("Lost", "customer_pct"))
print(s)
