"""BrewInsights data-cleaning entry points."""
import pandas as pd

def load_raw(path):
    return pd.read_csv(path)

def remove_identifiers(df):
    return df.drop(columns=["respondentId", "email", "createdAt", "source"], errors="ignore")
