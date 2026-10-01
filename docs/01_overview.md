# 1. Project Overview

## 1.1 Business problem
An online retailer in India (Electronics, Fashion, Home, Beauty, Grocery, Sports) sells across 8 cities. Management asks: where does revenue come from, who are the most valuable and at-risk customers, do customers return, why are returns high, and what should we expect next quarter?

## 1.2 Objectives
- Clean and model raw transactional data into an analysis-ready warehouse
- Report core KPIs: revenue, orders, AOV, growth, returns, cancellations
- Segment customers with RFM and measure retention with cohorts
- Forecast revenue and give actionable recommendations

## 1.3 Architecture
- Raw CSVs -> `etl.py` (clean, validate, log) -> SQLite star schema (`fact_sales`, `dim_customer`, `dim_product`) -> SQL queries -> pandas analysis -> charts/tables -> auto-generated insights -> PDF
- Design rule: one script per stage, shared helpers in `utils.py`, SQL kept in `sql/queries.sql`, numbers never hand-typed (written to `metrics.json` and pulled into reports)

## 1.4 Key definitions (say these in the interview)
- **Net revenue** = quantity x unit price x (1 - discount%), counted only for Delivered orders
- **AOV** = net revenue / delivered orders; **Return rate** = returned orders / all orders
- **Active customer** = at least one delivered order

## 1.5 Stakeholders and use
- Management (growth), Marketing (win-back and loyalty), Operations (returns), Finance (forecast)

## 1.6 Two-minute pitch
I built an end-to-end analytics pipeline for an e-commerce business. I simulated realistic messy data, cleaned it with logged data-quality rules, modelled it as a star schema in SQL, and calculated KPIs. I segmented customers with RFM, found that a minority of customers drives about half the revenue, measured cohort retention, and built a backtested forecast. Everything runs with one command and produces a report with recommendations such as win-back campaigns, return reduction and category diversification.

## 1.7 Limitations (be honest)
- Data is simulated, so findings demonstrate method, not real market truth
- Forecast uses only 24 months; growth percentages are inflated by the early ramp-up
- No causal claims (observational data); recommendations should be A/B tested
