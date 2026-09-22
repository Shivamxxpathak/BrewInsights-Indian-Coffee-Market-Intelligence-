"""Check that the analysis notebook remains intact and references canonical artifacts."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
NOTEBOOK=ROOT/"notebooks/BrewInsights_Analysis.ipynb"
REQUIRED=["outputs/datasets/consumer_cluster_assignments.csv","outputs/datasets/adoption_model_comparison.csv","outputs/datasets/spending_model_comparison.csv","data/coffee_demand_by_period.csv","outputs/datasets/market_entry_ranking.csv"]
def main():
    nb=json.loads(NOTEBOOK.read_text(encoding="utf-8")); cells=nb.get("cells",[]); text="\n".join("".join(c.get("source",[])) for c in cells); missing=[p for p in REQUIRED if p not in text]
    print("Notebook artifact-reference check:", "PASS" if not missing else f"WARN missing {missing}"); print(f"Notebook cells: {len(cells)}; executed cells: {sum(bool(c.get('outputs')) for c in cells)}")
if __name__=="__main__": main()
