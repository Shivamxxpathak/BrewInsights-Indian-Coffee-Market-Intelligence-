"""City intelligence and market-entry scoring utilities."""
from __future__ import annotations
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def build_city_features(df,external):
    g=df.groupby("city",dropna=True).agg(monthlyCoffeeSpend=("monthlyCoffeeSpend","mean"),income=("monthlyIncome","mean"),purchase_intention=("purchaseIntention",lambda s:s.astype("string").str.contains("Would Buy",case=False,na=False).mean())).reset_index()
    return g.merge(external,on="city",how="left")

def score_market_entry(city_df):
    out=city_df.copy()
    for c in ["monthlyCoffeeSpend","income","cafe_density","income_index"]:
        if c in out: out[c]=pd.to_numeric(out[c],errors="coerce")
    out["spending_score"]=out["monthlyCoffeeSpend"].rank(pct=True); out["city_strength_score"]=(out["cafe_density"].rank(pct=True)+out["income_index"].rank(pct=True))/2; out["adoption_score"]=out.get("purchase_intention",pd.Series(0,index=out.index)).fillna(0); out["trend_score"]=.5
    out["market_entry_score"]=out[["spending_score","city_strength_score","adoption_score","trend_score"]].mean(axis=1); out["rank"]=out["market_entry_score"].rank(method="min",ascending=False).astype(int)
    return out.sort_values("rank").reset_index(drop=True)

def cluster_cities(city_df,n_clusters=3,random_state=42):
    features=[c for c in ["monthlyCoffeeSpend","cafe_density","income_index"] if c in city_df]; x=city_df[features].apply(pd.to_numeric,errors="coerce").fillna(city_df[features].median(numeric_only=True)); scaled=StandardScaler().fit_transform(x); model=KMeans(n_clusters=n_clusters,random_state=random_state,n_init=20); labels=model.fit_predict(scaled); out=city_df.copy(); out["cluster"]=labels; return out,pd.DataFrame([{"method":"KMeans","n_clusters":n_clusters,"silhouette_score":silhouette_score(scaled,labels)}])

def load_ranking(path="outputs/datasets/market_entry_ranking.csv"): return pd.read_csv(path)
def load_sensitivity(path="outputs/datasets/recommendation_sensitivity.csv"): return pd.read_csv(path)
