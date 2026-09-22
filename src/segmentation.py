"""Reusable consumer and city segmentation routines."""
from __future__ import annotations
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

DEFAULT_CONSUMER_FEATURES=["age","monthlyIncome","monthlyCoffeeSpend","preferredPriceRange"]

def _matrix(df, features):
    x=df[features].apply(pd.to_numeric,errors="coerce"); x=x.fillna(x.median()); return StandardScaler().fit_transform(x),x

def segment_consumers(df, features=None, n_clusters=3, random_state=42):
    features=features or DEFAULT_CONSUMER_FEATURES; missing=[c for c in features if c not in df]
    if missing: raise ValueError(f"Missing segmentation features: {missing}")
    scaled,_=_matrix(df,features); model=KMeans(n_clusters=n_clusters,random_state=random_state,n_init=20); labels=model.fit_predict(scaled)
    assignments=df.copy(); assignments["cluster"]=labels
    profiles=assignments.groupby("cluster")[features].mean(numeric_only=True).reset_index()
    metrics=pd.DataFrame([{"method":"KMeans","n_clusters":n_clusters,"silhouette_score":silhouette_score(scaled,labels)}])
    return assignments,profiles,metrics

def compare_clustering(df, features=None, n_clusters=3, random_state=42):
    features=features or DEFAULT_CONSUMER_FEATURES; scaled,_=_matrix(df,features)
    km=KMeans(n_clusters=n_clusters,random_state=random_state,n_init=20).fit(scaled); agg=AgglomerativeClustering(n_clusters=n_clusters).fit(scaled)
    return pd.DataFrame([{"method":"KMeans","n_clusters":n_clusters,"silhouette_score":silhouette_score(scaled,km.labels_)},{"method":"Agglomerative","n_clusters":n_clusters,"silhouette_score":silhouette_score(scaled,agg.labels_)}])

def load_consumer_assignments(path="outputs/datasets/consumer_cluster_assignments.csv"): return pd.read_csv(path)
def load_city_clusters(path="outputs/datasets/city_cluster_assignments.csv"): return pd.read_csv(path)
