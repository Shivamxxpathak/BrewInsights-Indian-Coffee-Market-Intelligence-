"""Repository-level pipeline entry point.

The executed notebook remains the analytical source of truth.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    print("BrewInsights artifacts are stored in data/ and outputs/datasets/.")
    print("Run notebooks/BrewInsights_Analysis.ipynb for the full original workflow.")
