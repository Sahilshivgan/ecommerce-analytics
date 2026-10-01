# 3. Methodology: When, Why, How, Where

## 3.1 ETL and data cleaning
- **When:** always before analysis; every real dataset has duplicates, nulls, bad types.
- **Why:** wrong inputs give confident wrong answers (duplicates inflate revenue, outliers skew averages).
- **How:** pandas `drop_duplicates`, `fillna`, `to_datetime(errors="coerce")`, range filters, then load to SQL; log counts.
- **Where:** every analytics/BI/ML job; in production this runs on Airflow/dbt/ADF on a schedule.

## 3.2 Star schema and SQL
- **When:** repeated reporting on transactions; many questions on the same facts.
- **Why:** facts + dimensions make joins simple, queries fast, and metrics consistent.
- **How:** `JOIN`, `GROUP BY`, `CASE WHEN`, `COUNT(DISTINCT)`, window `RANK() OVER (PARTITION BY ...)`.
- **Where:** data warehouses (Snowflake, BigQuery, Redshift, Postgres) feeding Power BI/Tableau.

## 3.3 KPI analysis
- **When:** monthly business reviews, dashboards. **Why:** KPIs turn raw rows into decisions (growth, margin proxies, risk).
- **How:** monthly aggregation, AOV, MoM growth with `pct_change`, category/city splits, return and cancel rates.
- **Where:** exec dashboards, finance and ops reviews.

## 3.4 RFM segmentation
- **When:** you need to prioritise marketing spend among customers. **Why:** customers are not equal; recency, frequency, monetary predict value and churn risk cheaply and explainably.
- **How:** Recency (days since last order, quintiles, recent = high), Frequency (business bins clipped 1-5 because many ties break quantiles), Monetary (quintiles); rules map scores to Champions, Loyal, New, At Risk, Lost.
- **Where:** CRM, email/push campaigns, loyalty programs, retail and banking.

## 3.5 Cohort retention
- **When:** to learn whether customers come back and whether newer cohorts are better. **Why:** averages hide churn; cohorts separate acquisition month from behaviour over time.
- **How:** cohort = first purchase month; index = months since; retention = active customers / cohort size.
- **Where:** SaaS, e-commerce, apps, subscription businesses; product and growth teams.

## 3.6 Forecasting
- **When:** planning stock, ad budget, targets. **Why:** decisions need numbers about the future with a known error.
- **How:** raw trend models failed here (ramp-up growth gave a negative forecast), so revenue was normalised per registered customer, last year's seasonal shape was applied to the latest level, and error was measured by backtesting (MAPE).
- **Where:** demand planning, finance, capacity planning. Upgrade path: Holt-Winters, SARIMA, Prophet, gradient boosting with more history.

## 3.7 Tool choices
- **pandas** for in-memory analysis up to a few million rows; move to Spark/SQL engines beyond that.
- **SQLite** for a zero-setup demo; in production use PostgreSQL/Snowflake (same SQL).
- **matplotlib** for static charts; use Power BI/Tableau for interactive dashboards.
- **Auto-generated docs** guarantee report numbers match the data.
