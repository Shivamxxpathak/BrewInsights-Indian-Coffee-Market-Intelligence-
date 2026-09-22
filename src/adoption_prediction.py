"""New-brand adoption result loader."""
import pandas as pd

def load_results(path="outputs/datasets/adoption_model_comparison.csv"):
    return pd.read_csv(path)
