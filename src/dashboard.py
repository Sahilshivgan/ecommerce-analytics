"""Step 9 - One-page dashboard image + animated demo GIF for the README."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from utils import *

m = load_metrics(); mk = pd.read_csv(TAB / "monthly_kpi.csv"); cat = pd.read_csv(TAB / "category_perf.csv")
city = pd.read_csv(TAB / "city_perf.csv"); seg = pd.read_csv(TAB / "rfm_segments.csv"); fc = pd.read_csv(TAB / "forecast.csv")
ret = pd.read_csv(TAB / "cohort_retention.csv", index_col=0).iloc[:, 1:13]
NAVY, BLUE, LIGHT = "#1b4965", "#2a6f97", "#eef3f7"

fig = plt.figure(figsize=(15, 9.5), facecolor="white")
fig.text(.5, .965, "E-Commerce Sales & Customer Analytics Dashboard", ha="center", fontsize=20, weight="bold", color=NAVY)
cards = [("Net Revenue", f"INR {m['total_revenue']/1e6:.0f}M"), ("Delivered Orders", f"{m['orders']:,}"), ("Avg Order Value", f"INR {m['aov']:,.0f}"),
         ("Return Rate", f"{m['return_rate_pct']}%"), ("Month-1 Retention", f"{m['month1_retention_pct']}%"), ("Forecast MAPE", f"{m['forecast_mape_pct']}%")]
for i, (t, v) in enumerate(cards):
    x = .03 + i * .1583
    fig.patches.append(plt.Rectangle((x, .84), .145, .095, transform=fig.transFigure, color=LIGHT, zorder=0))
    fig.text(x + .0725, .90, v, ha="center", fontsize=17, weight="bold", color=BLUE); fig.text(x + .0725, .858, t, ha="center", fontsize=9.5, color="#555")
gs = fig.add_gridspec(2, 3, left=.09, right=.97, top=.78, bottom=.07, hspace=.5, wspace=.3)
ax = fig.add_subplot(gs[0, 0]); ax.plot(mk.month, mk.revenue / 1e6, color=BLUE, marker="o", ms=3)
ax.plot([mk.month.iloc[-1]] + list(fc.month), [mk.revenue.iloc[-1] / 1e6] + list(fc.forecast_revenue / 1e6), "r--o", ms=3)
ax.set_title("Monthly revenue + forecast (INR M)", fontsize=10); ax.set_xticks(range(0, len(mk), 6)); ax.set_xticklabels(list(mk.month)[::6], rotation=45, fontsize=7)
ax = fig.add_subplot(gs[0, 1]); ax.bar(cat.category, cat.revenue / 1e6, color=BLUE); ax.set_title("Revenue by category (INR M)", fontsize=10); ax.tick_params(axis="x", rotation=30, labelsize=8)
ax = fig.add_subplot(gs[0, 2]); ax.barh(city.city[::-1], city.revenue[::-1] / 1e6, color=BLUE); ax.set_title("Revenue by city (INR M)", fontsize=10); ax.tick_params(labelsize=8)
ax = fig.add_subplot(gs[1, 0]); ax.barh(seg.segment[::-1], seg.revenue_pct[::-1], color=NAVY); ax.set_title("Revenue share by RFM segment (%)", fontsize=10); ax.tick_params(labelsize=8)
ax = fig.add_subplot(gs[1, 1]); im = ax.imshow(ret.values, cmap="Blues", vmin=0, vmax=40, aspect="auto", extent=(0.5, 12.5, len(ret), 0))
ax.set_title("Cohort retention (%)", fontsize=10); ax.set_xlabel("Months since first purchase", fontsize=8); ax.set_yticks([]); ax.tick_params(labelsize=8)
ax = fig.add_subplot(gs[1, 2]); ax.bar(cat.category, cat.return_rate_pct, color="#c1666b"); ax.set_title("Return rate by category (%)", fontsize=10); ax.tick_params(axis="x", rotation=30, labelsize=8)
for a in fig.axes: a.spines[["top", "right"]].set_visible(False)
fig.savefig(FIG / "dashboard.png", dpi=110); plt.close()

frames = []
for n in ["dashboard", "monthly_revenue", "category_revenue", "rfm_segments", "cohort_retention", "forecast"]:
    im = Image.open(FIG / f"{n}.png").convert("RGB"); w = 1000
    im = im.resize((w, int(im.height * w / im.width))); canvas = Image.new("RGB", (w, 680), "white")
    canvas.paste(im, (0, (680 - im.height) // 2)); frames.append(canvas.quantize(colors=128))
frames[0].save(FIG / "demo.gif", save_all=True, append_images=frames[1:], duration=2200, loop=0, optimize=True)
print("dashboard + gif built")
