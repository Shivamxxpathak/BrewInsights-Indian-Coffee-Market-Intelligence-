"""Coffee-spending result loader."""
import pandas as pd

def load_results(path="outputs/datasets/spending_model_comparison.csv"):
    return pd.read_csv(path)
