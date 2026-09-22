"""Segmentation result loaders."""
import pandas as pd

def load_consumer_assignments(path="outputs/datasets/consumer_cluster_assignments.csv"):
    return pd.read_csv(path)

def load_city_clusters(path="outputs/datasets/city_cluster_assignments.csv"):
    return pd.read_csv(path)
