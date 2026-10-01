"""Step 5 - Monthly cohort retention."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils import *

d = query("cohort_base"); d["om"] = pd.PeriodIndex(d.order_month, freq="M")
d["cm"] = d.groupby("customer_id").om.transform("min")
d["idx"] = (d.om - d.cm).apply(lambda x: x.n)
p = d.pivot_table(index="cm", columns="idx", values="customer_id", aggfunc="nunique")
ret = (p.div(p[0], axis=0) * 100).round(1); ret.to_csv(TAB / "cohort_retention.csv")
r = ret.iloc[:, 1:13]
fig, ax = plt.subplots(figsize=(9, 6)); im = ax.imshow(r.values, cmap="Blues", vmin=0, vmax=40, aspect="auto", extent=(0.5, 12.5, len(r), 0))
ax.set_yticks(np.arange(len(r)) + .5); ax.set_yticklabels(r.index.astype(str), fontsize=7)
ax.set_xlabel("Months since first purchase"); ax.set_title("Cohort retention (%)"); fig.colorbar(im)
fig.tight_layout(); fig.savefig(FIG / "cohort_retention.png", dpi=130); plt.close()
save_metrics(month1_retention_pct=round(float(np.nanmean(ret[1])), 1), month3_retention_pct=round(float(np.nanmean(ret[3])), 1))
print("Cohort done")
