# 5. Interview Questions and Answers

## 5.1 Project and business
**Q1. Explain your project in 1 minute.**
End-to-end e-commerce analytics: simulated messy transactional data, cleaned and loaded into a SQL star schema, KPIs, RFM segmentation, cohort retention, a backtested forecast, and a report with recommendations. One command reproduces everything.

**Q2. Why e-commerce and why this data?**
It has all classic analytics problems: transactions, customers, products, returns, seasonality. Simulation let me inject realistic dirt and know the truth, so I could validate my methods.

**Q3. What business value did it produce?**
It shows revenue concentration (category and customer), a high-value Champions segment, at-risk customers to win back, return hotspots, weak early retention, and a forecast with known error, each tied to an action.

**Q4. How would you present to a non-technical client?**
Lead with 3 headline numbers and 3 actions, use the charts, avoid jargon, explain RFM as "best, at-risk and lost customers", and state limits.

**Q5. What are the project limitations?**
Simulated data, 24 months of history, observational (no causality), growth inflated by ramp-up, simple forecast. With real data I would add margin, marketing spend and A/B tests.

## 5.2 Data cleaning and ETL
**Q6. What data quality issues did you handle?**
Duplicate orders, null payment methods, negative quantities, impossible ages, inconsistent city text. Each rule logs how many rows it touched.

**Q7. Why fill payment nulls instead of dropping rows?**
The order is real revenue; dropping it would understate sales. Labelling "Unknown" keeps the row and the gap visible.

**Q8. Mean or median to fix outliers?**
Median, because it is robust to outliers; the mean is pulled by the very values being fixed.

**Q9. How do you avoid double counting?**
Fact grain is one order line, so orders are counted with `COUNT(DISTINCT order_id)`, and revenue is summed at line level.

**Q10. Why exclude Cancelled and Returned from revenue?**
Net revenue should reflect money actually kept. Returns are still measured separately as a risk metric.

**Q11. How would you productionise the ETL?**
Schedule with Airflow or dbt, add tests (uniqueness, not-null, ranges), incremental loads, alerting, and version control.

## 5.3 SQL
**Q12. WHERE vs HAVING?**
WHERE filters rows before grouping; HAVING filters groups after aggregation.

**Q13. INNER vs LEFT JOIN?**
INNER keeps matches only; LEFT keeps all left rows with NULLs where no match (useful to find customers with no orders).

**Q14. Where did you use a window function?**
`RANK() OVER (PARTITION BY city ORDER BY revenue DESC)` to find the top category per city without a self-join.

**Q15. COUNT(*) vs COUNT(DISTINCT x)?**
COUNT(*) counts rows; COUNT(DISTINCT x) counts unique values, essential at line-level grain.

**Q16. How do you speed up a slow query?**
Index filter/join columns, select only needed columns, filter early, avoid functions on indexed columns, check the query plan, pre-aggregate.

**Q17. Why a star schema?**
Simple joins, consistent metrics, fast aggregates, and easy BI connection compared with a flat or highly normalised design.

## 5.4 Analysis methods
**Q18. What is RFM and why use it?**
Recency, Frequency, Monetary scoring of customers. It is simple, explainable and effective for prioritising marketing.

**Q19. Why did you not use quantiles for Frequency?**
Most customers have 1-3 orders, so quantiles create ties and arbitrary splits. I used business bins clipped at 5.

**Q20. How do you pick RFM segment rules?**
From business meaning (e.g. high R and high F = Champions), then check sizes and revenue share, and adjust. K-means is an alternative but less explainable.

**Q21. What is a cohort analysis?**
Group customers by first purchase month and track the share still buying in later months. It reveals retention beyond blended averages.

**Q22. What did retention tell you?**
Month-1 retention is low and flat afterwards, so the first 30 days decide loyalty; the action is onboarding and a second-purchase incentive.

**Q23. How did you forecast and how did you validate?**
Linear and log trends failed because of ramp-up growth. I normalised revenue per registered customer, applied last year's seasonal shape to the latest level, and backtested on the last 3 months with MAPE.

**Q24. What is MAPE and its weakness?**
Mean absolute percentage error. Easy to interpret but unstable near zero values and treats over/under forecasts equally.

**Q25. Why is YoY growth very high?**
The business was still acquiring customers in 2023, so the base year is tiny. I flagged it rather than presenting it as organic growth.

**Q26. Correlation vs causation here?**
Data is observational: segments and retention show association, not proof. I would run A/B tests on win-back offers.

## 5.5 Scenario and judgement
**Q27. Revenue dropped 15% last month. What do you do?**
Check data first (missing loads, definitions), then decompose by orders x AOV, category, city, channel, new vs returning, and compare with last year's seasonality; then form hypotheses.

**Q28. Marketing has a small budget. Whom do you target?**
At Risk customers with high past value (cheapest win-back), protect Champions with loyalty perks, and avoid spending on Lost customers.

**Q29. How would you scale this to 100 million rows?**
Move to a warehouse (BigQuery/Snowflake) or Spark, push aggregation to SQL, partition by date, and schedule incremental pipelines.

**Q30. What would you improve next?**
Margin and CAC data, customer lifetime value, churn prediction model, proper time-series models, an interactive dashboard (Power BI/Streamlit), and CI tests for the pipeline.

**Q31. How do you ensure results are reproducible?**
Fixed random seed, one-command pipeline, SQL in version control, metrics stored in JSON and inserted automatically into the report.

**Q32. Which chart type for which message?**
Line for trends, bar for category comparison, heatmap for cohorts, horizontal bar for ranked shares. Always title, units and one takeaway.
