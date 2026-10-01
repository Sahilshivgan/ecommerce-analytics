"""Step 6 - Revenue forecast.
Method: normalise revenue by registered-customer base (removes growth from new signups),
then project revenue-per-customer with last year's seasonal shape anchored on the latest level
(seasonal-naive with level adjustment). Backtested on the last 3 months (MAPE)."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils import *

m = query("monthly_revenue"); y = m.revenue.values.astype(float)
sg = query("signups").set_index("month").n
base = sg.reindex(m.month).fillna(0).cumsum().values.astype(float)
rpc = y / base                                              # revenue per registered customer

def project(anchor, h):
    return np.array([rpc[anchor] * rpc[anchor + k - 12] / rpc[anchor - 12] for k in range(1, h + 1)])

h = 3
pred = project(len(y) - h - 1, h) * base[-h:]               # backtest: hide last 3 months
mape = float(np.mean(np.abs((y[-h:] - pred) / y[-h:])) * 100)
new_rate = sg.reindex(m.month).fillna(0).values[-3:].mean() # assume recent signup pace continues
fut_base = base[-1] + new_rate * np.arange(1, h + 1)
fc = project(len(y) - 1, h) * fut_base
fut_p = pd.period_range(pd.Period(m.month.iloc[-1], "M") + 1, periods=h, freq="M")
out = pd.DataFrame({"month": fut_p.astype(str), "forecast_revenue": fc.round(0)}); out.to_csv(TAB / "forecast.csv", index=False)

fig, ax = plt.subplots(figsize=(9, 4)); ax.plot(m.month, y / 1e6, label="Actual")
ax.plot([m.month.iloc[-1]] + list(out.month), [y[-1] / 1e6] + list(fc / 1e6), "r--o", label="Forecast")
ax.legend(); ax.grid(alpha=.3); ax.set_xticks(list(range(0, len(m), 3)) + [len(m) + 1])
ax.set_xticklabels(list(m.month[::3]) + [out.month[1]], rotation=45)
ax.set_title("Revenue forecast (INR million)"); fig.tight_layout(); fig.savefig(FIG / "forecast.png", dpi=130); plt.close()
save_metrics(forecast_mape_pct=round(mape, 1), forecast_next_3m=float(fc.sum()), forecast_start=str(fut_p[0]))
print("MAPE", round(mape, 1)); print(out)
