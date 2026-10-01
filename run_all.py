"""Run the whole project end-to-end: python run_all.py  (about 1 minute)."""
import subprocess, sys
from pathlib import Path
for s in ["generate_data", "etl", "kpi", "rfm", "cohort", "forecast", "report", "dashboard", "build_pdf"]:
    print(f"\n== {s} ==")
    subprocess.run([sys.executable, str(Path(__file__).parent / "src" / f"{s}.py")], check=True)
