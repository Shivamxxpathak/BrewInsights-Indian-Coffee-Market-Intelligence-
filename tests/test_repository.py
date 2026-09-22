from pathlib import Path
import ast
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md", "requirements.txt", "notebooks/BrewInsights_Analysis.ipynb",
    "dashboard/app.py", "dashboard/requirements_dashboard.txt", "dashboard/run_dashboard.py",
    "data/processed/coffee_cleaned.csv", "data/coffee_demand_by_period.csv", "data/coffee_demand_forecast.csv",
    "outputs/datasets/consumer_cluster_assignments.csv", "outputs/datasets/city_opportunity_scores.csv",
    "outputs/datasets/market_entry_ranking.csv", "docs/DATA_DICTIONARY.md", "docs/METHODOLOGY.md",
    "docs/MODEL_EVALUATION.md",
]

def test_required_project_files_exist():
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).exists()]
    assert not missing, f"Missing required project files: {missing}"

def test_processed_survey_schema_and_size():
    df = pd.read_csv(ROOT / "data/processed/coffee_cleaned.csv")
    required = {
        "age", "gender", "city", "occupation", "monthlyIncome", "coffeeFrequency",
        "preferredCoffeeType", "preferredBrand", "monthlyCoffeeSpend", "purchaseLocation",
        "purchaseMode", "priceSensitivity", "tastePreference", "brandLoyalty",
        "willingnessToTry", "preferredPriceRange", "purchaseIntention",
    }
    assert required.issubset(df.columns)
    assert len(df) > 0
    assert "email" not in df.columns
    assert "respondentId" not in df.columns

def test_key_output_files_are_nonempty():
    paths = ["outputs/datasets/consumer_cluster_assignments.csv", "outputs/datasets/city_opportunity_scores.csv", "outputs/datasets/market_entry_ranking.csv", "data/coffee_demand_by_period.csv", "data/coffee_demand_forecast.csv"]
    for path in paths:
        df = pd.read_csv(ROOT / path)
        assert not df.empty, f"{path} is empty"

def test_dashboard_python_syntax():
    source = (ROOT / "dashboard/app.py").read_text(encoding="utf-8")
    ast.parse(source, filename="dashboard/app.py")