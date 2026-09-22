from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"

subprocess.run([sys.executable, "-m", "streamlit", "run", str(APP)], check=True)
