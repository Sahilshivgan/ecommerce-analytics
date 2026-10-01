"""Step 3 - Core business KPIs + trend/category/city charts."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils import *

m = query("monthly_revenue")
m["aov"] = (m.revenue / m.orders).round(0)
m["mom_growth_pct"] = (m.revenue.pct_change() * 100).round(1)
m.to_csv(TAB / "monthly_kpi.csv", index=False)
cat, city = query("category_perf"), query("city_perf")
cat.to_csv(TAB / "category_perf.csv", index=False); city.to_csv(TAB / "city_perf.csv", index=False)
query("payment_mix").to_csv(TAB / "payment_mix.csv", index=False)
rk = query("city_category_rank"); rk[rk.rnk == 1].to_csv(TAB / "top_category_per_city.csv", index=False)
sm = query("status_mix").set_index("status").orders; tot = sm.sum()

fig, ax = plt.subplots(figsize=(9, 4)); ax.plot(m.month, m.revenue / 1e6, marker="o")
ax.set_title("Monthly Net Revenue (INR million)"); ax.set_xticks(range(0, len(m), 3)); ax.set_xticklabels(m.month[::3], rotation=45)
ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(FIG / "monthly_revenue.png", dpi=130); plt.close()
fig, ax = plt.subplots(figsize=(9, 4)); ax.bar(cat.category, cat.revenue / 1e6, color="#2a6f97")
ax.set_title("Net Revenue by Category (INR million)"); fig.tight_layout(); fig.savefig(FIG / "category_revenue.png", dpi=130); plt.close()

y23 = m[m.month.str.startswith("2023")].revenue.sum(); y24 = m[m.month.str.startswith("2024")].revenue.sum()
pk = m.loc[m.revenue.idxmax()]
save_metrics(total_revenue=float(m.revenue.sum()), orders=int(m.orders.sum()), aov=float(round(m.revenue.sum() / m.orders.sum())),
    return_rate_pct=round(float(100 * sm.get("Returned", 0) / tot), 1), cancel_rate_pct=round(float(100 * sm.get("Cancelled", 0) / tot), 1),
    top_category=str(cat.category[0]), top_category_share_pct=round(float(100 * cat.revenue[0] / cat.revenue.sum()), 1),
    top_city=str(city.city[0]), top_city_share_pct=round(float(100 * city.revenue[0] / city.revenue.sum()), 1),
    yoy_growth_pct=round(float(100 * (y24 / y23 - 1)), 1), peak_month=str(pk.month), peak_month_revenue=float(pk.revenue),
    highest_return_category=str(cat.sort_values("return_rate_pct").category.iloc[-1]))
print("KPI done")
