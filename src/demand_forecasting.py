"""Demand forecasting result loaders."""
import pandas as pd

def load_demand(path="data/coffee_demand_by_period.csv"):
    return pd.read_csv(path)

def load_forecast(path="data/coffee_demand_forecast.csv"):
    return pd.read_csv(path)

def load_model_comparison(path="data/coffee_demand_model_comparison.csv"):
    return pd.read_csv(path)
