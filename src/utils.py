"""Shared paths + helpers (DB connection, named SQL queries, metrics store)."""
import sqlite3, json, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC = ROOT / "data/raw", ROOT / "data/processed"
FIG, TAB = ROOT / "reports/figures", ROOT / "reports/tables"
DB = PROC / "warehouse.db"
for p in (RAW, PROC, FIG, TAB):
    p.mkdir(parents=True, exist_ok=True)

def conn():
    return sqlite3.connect(DB)

def query(name):
    """Run a named query from sql/queries.sql ('-- name: xyz' blocks)."""
    sql = (ROOT / "sql/queries.sql").read_text()
    blocks = dict(re.findall(r"-- name: (\w+)\n(.*?)(?=\n-- name:|\Z)", sql, re.S))
    c = conn()
    try:
        return pd.read_sql(blocks[name], c)
    finally:
        c.close()

def save_metrics(**kw):
    f = ROOT / "reports/metrics.json"
    d = json.loads(f.read_text()) if f.exists() else {}
    d.update(kw)
    f.write_text(json.dumps(d, indent=2))

def load_metrics():
    return json.loads((ROOT / "reports/metrics.json").read_text())
