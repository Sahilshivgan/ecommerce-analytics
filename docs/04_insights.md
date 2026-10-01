# 4. Results, Insights and Recommendations

## 4.1 Headline KPIs (delivered orders only)
- Net revenue: **INR 342.2M** from **18,202** delivered orders
- Average order value (AOV): **INR 18,798**; active buying customers: **4,370**
- Return rate **6.2%**, cancellation rate **4.0%**
- Peak month: **2024-11** (INR 36.4M) - festive-season effect
- Year-on-year growth: **230.5%** (CAUTION: inflated because the customer base was still ramping up in 2023; a mature business would be far lower)

![Monthly revenue](reports/figures/monthly_revenue.png)

## 4.2 Where the money comes from
- Top category: **Electronics** = 65.1% of revenue (concentration risk)
- Top city: **Mumbai** = 20.9% of revenue
- Highest return-rate category: **Sports**
- **Electronics**: revenue INR 222.9M, return rate 6.0%, avg discount 6.6%
- **Home**: revenue INR 45.9M, return rate 5.8%, avg discount 6.6%
- **Sports**: revenue INR 36.9M, return rate 6.6%, avg discount 6.6%
- **Fashion**: revenue INR 23.5M, return rate 6.3%, avg discount 6.4%
- **Beauty**: revenue INR 8.9M, return rate 6.0%, avg discount 6.6%
- **Grocery**: revenue INR 4.1M, return rate 6.2%, avg discount 6.4%

![Category revenue](reports/figures/category_revenue.png)

## 4.3 Customer segments (RFM)
- **Champions**: 1189 customers (27.2%), 47.4% of revenue, avg value INR 136,372
- **Loyal**: 896 customers (20.5%), 28.2% of revenue, avg value INR 107,843
- **Needs Attention**: 647 customers (14.8%), 8.5% of revenue, avg value INR 45,107
- **Lost**: 1018 customers (23.3%), 7.9% of revenue, avg value INR 26,613
- **At Risk**: 304 customers (7.0%), 5.0% of revenue, avg value INR 56,477
- **New / Promising**: 316 customers (7.2%), 2.9% of revenue, avg value INR 31,472

- Champions are 27.2% of customers but **47.4%** of revenue (Pareto effect)
- At Risk customers (304) hold 5.0% of revenue: cheapest win-back target

![RFM](reports/figures/rfm_segments.png)

## 4.4 Retention (cohorts)
- Average month-1 retention: **22.6%**; month-3: **23.1%**
- Reading: customers who do not come back in month 1 rarely return later, so onboarding and the first 30 days matter most

![Cohorts](reports/figures/cohort_retention.png)

## 4.5 Forecast (next 3 months, starting 2025-01)
- 2025-01: INR 20.1M
- 2025-02: INR 20.0M
- 2025-03: INR 24.2M
- Backtest error (MAPE on last 3 known months): **3.4%**. Seasonal dip after the festive peak is expected.

![Forecast](reports/figures/forecast.png)

## 4.6 Recommendations
- **Diversify:** Electronics drives 65.1% of revenue; grow Home/Beauty/Fashion to reduce single-category risk.
- **Reduce returns:** investigate Sports (size/quality/description issues); each 1 point of return rate recovers revenue and logistics cost.
- **Win-back campaign:** target the At Risk segment with personalised offers before they become Lost.
- **Protect Champions:** early access, loyalty tiers; they carry nearly half of revenue.
- **Fix month-1 retention:** welcome journey, second-purchase coupon within 30 days.
- **Plan for seasonality:** stock and ad budget ahead of Oct-Dec; expect a Q1 dip.

## 4.7 Data quality log (ETL)
- Raw orders 20,469; duplicates removed 203; null payment methods filled 409
- Invalid quantities removed 151 of 50,460 item rows; age outliers fixed 50; final fact rows 50,309

## 4.8 Resume bullets
- Built an end-to-end e-commerce analytics pipeline (Python, SQL, SQLite star schema) on 18,202 orders and INR 342.2M revenue, with automated cleaning and data-quality logging.
- Segmented 4,370 customers with RFM, showing 27.2% of customers drive 47.4% of revenue, and quantified cohort retention and return hotspots.
- Delivered a customer-base-normalised revenue forecast with 3.4% backtest MAPE plus an auto-generated PDF report and business recommendations.
