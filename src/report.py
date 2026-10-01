"""Step 7 - Auto-generate docs/04_insights.md from computed metrics (numbers never hand-typed)."""
import json, pandas as pd
from utils import *

m = load_metrics(); dq = json.loads((ROOT / "reports/data_quality.json").read_text())
seg = pd.read_csv(TAB / "rfm_segments.csv"); fc = pd.read_csv(TAB / "forecast.csv"); cat = pd.read_csv(TAB / "category_perf.csv")
M = lambda x: f"INR {x/1e6:,.1f}M"
segs = "\n".join(f"- **{r.segment}**: {int(r.customers)} customers ({r.customer_pct}%), {r.revenue_pct}% of revenue, avg value INR {int(r.avg_value):,}" for r in seg.itertuples())
fcs = "\n".join(f"- {r.month}: {M(r.forecast_revenue)}" for r in fc.itertuples())
cats = "\n".join(f"- **{r.category}**: revenue {M(r.revenue)}, return rate {r.return_rate_pct}%, avg discount {r.avg_discount_pct}%" for r in cat.itertuples())
txt = f"""# 4. Results, Insights and Recommendations

## 4.1 Headline KPIs (delivered orders only)
- Net revenue: **{M(m['total_revenue'])}** from **{m['orders']:,}** delivered orders
- Average order value (AOV): **INR {m['aov']:,.0f}**; active buying customers: **{m['active_customers']:,}**
- Return rate **{m['return_rate_pct']}%**, cancellation rate **{m['cancel_rate_pct']}%**
- Peak month: **{m['peak_month']}** ({M(m['peak_month_revenue'])}) - festive-season effect
- Year-on-year growth: **{m['yoy_growth_pct']}%** (CAUTION: inflated because the customer base was still ramping up in 2023; a mature business would be far lower)

![Monthly revenue](reports/figures/monthly_revenue.png)

## 4.2 Where the money comes from
- Top category: **{m['top_category']}** = {m['top_category_share_pct']}% of revenue (concentration risk)
- Top city: **{m['top_city']}** = {m['top_city_share_pct']}% of revenue
- Highest return-rate category: **{m['highest_return_category']}**
{cats}

![Category revenue](reports/figures/category_revenue.png)

## 4.3 Customer segments (RFM)
{segs}

- Champions are {m['champions_customer_pct']}% of customers but **{m['champions_revenue_pct']}%** of revenue (Pareto effect)
- At Risk customers ({m['at_risk_customers']}) hold {m['at_risk_revenue_pct']}% of revenue: cheapest win-back target

![RFM](reports/figures/rfm_segments.png)

## 4.4 Retention (cohorts)
- Average month-1 retention: **{m['month1_retention_pct']}%**; month-3: **{m['month3_retention_pct']}%**
- Reading: customers who do not come back in month 1 rarely return later, so onboarding and the first 30 days matter most

![Cohorts](reports/figures/cohort_retention.png)

## 4.5 Forecast (next 3 months, starting {m['forecast_start']})
{fcs}
- Backtest error (MAPE on last 3 known months): **{m['forecast_mape_pct']}%**. Seasonal dip after the festive peak is expected.

![Forecast](reports/figures/forecast.png)

## 4.6 Recommendations
- **Diversify:** {m['top_category']} drives {m['top_category_share_pct']}% of revenue; grow Home/Beauty/Fashion to reduce single-category risk.
- **Reduce returns:** investigate {m['highest_return_category']} (size/quality/description issues); each 1 point of return rate recovers revenue and logistics cost.
- **Win-back campaign:** target the At Risk segment with personalised offers before they become Lost.
- **Protect Champions:** early access, loyalty tiers; they carry nearly half of revenue.
- **Fix month-1 retention:** welcome journey, second-purchase coupon within 30 days.
- **Plan for seasonality:** stock and ad budget ahead of Oct-Dec; expect a Q1 dip.

## 4.7 Data quality log (ETL)
- Raw orders {dq['raw_orders']:,}; duplicates removed {dq['duplicate_orders_removed']}; null payment methods filled {dq['null_payment_filled']}
- Invalid quantities removed {dq['invalid_quantity_removed']} of {dq['raw_items']:,} item rows; age outliers fixed {dq['age_outliers_fixed']}; final fact rows {dq['fact_rows']:,}

## 4.8 Resume bullets
- Built an end-to-end e-commerce analytics pipeline (Python, SQL, SQLite star schema) on {m['orders']:,} orders and {M(m['total_revenue'])} revenue, with automated cleaning and data-quality logging.
- Segmented {m['active_customers']:,} customers with RFM, showing {m['champions_customer_pct']}% of customers drive {m['champions_revenue_pct']}% of revenue, and quantified cohort retention and return hotspots.
- Delivered a customer-base-normalised revenue forecast with {m['forecast_mape_pct']}% backtest MAPE plus an auto-generated PDF report and business recommendations.
"""
(ROOT / "docs/04_insights.md").write_text(txt)
print("insights written")
