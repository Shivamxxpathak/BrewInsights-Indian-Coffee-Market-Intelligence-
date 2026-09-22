"""Market-entry result loaders."""
import pandas as pd

def load_ranking(path="outputs/datasets/market_entry_ranking.csv"):
    return pd.read_csv(path)

def load_sensitivity(path="outputs/datasets/recommendation_sensitivity.csv"):
    return pd.read_csv(path)
