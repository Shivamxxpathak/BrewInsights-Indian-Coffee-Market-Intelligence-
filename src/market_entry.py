"""Notebook-parity city intelligence and market-entry scoring utilities."""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def _city_base(df):
    d=df.copy()
    d=d.drop(columns=["tastePreference","occupation","gender"],errors="ignore")
    d["young_age"]=(pd.to_numeric(d["age"],errors="coerce")<=30)
    for c,m in {
        "coffeeFrequency":{"3-4 times/week":0,"Daily":1,"1-2 times/week":2,"Rarely":3,"Multiple times/day":4,"sometimes":5,"few":6},
        "brandLoyalty":{"Medium":1,"High":2,"Low":0,"I Like To Explore":1,"Very Loyal":2,"Somewhat Loyal":1,"No Preference":0},
        "purchaseIntention":{"Medium":1,"High":2,"Low":0,"Probably Would Buy":1,"Not Sure":0,"Definitely Would Buy":2,"Probably Would Not Buy":1},
        "purchaseMode":{"Offline":0,"Both":1,"Online":2,"Both equally":1},
        "willingnessToTry":{"Likely":2,"Neutral":1,"Very Likely":2,"Unlikely":0,"Very Unlikely":0,"Somewhat Willing":1,"Very Willing":2,"Not Currently Interested":0}
    }.items():
        if c in d: d[c]=d[c].map(m)
    d["priceSensitivity"]=d.get("priceSensitivity",pd.Series(index=d.index)).map({"High":2,"Low":0,"Medium":1,"Neutral":3,"Somewhat Sensitive":4,"Very Sensitive":5,"Not Very Sensitive":6})
    city=d.groupby("city")[["monthlyCoffeeSpend","priceSensitivity"]].mean().reset_index()
    brand_map={"Nescafe":"Mass/Instant","Bru":"Mass/Instant","Davidoff":"Mass/Instant","Blue Tokai":"Premium","Sleepy Owl":"Premium","Third Wave Coffee":"Premium","Rage Coffee":"Premium","Starbucks":"Café Chain","Café Coffee Day":"Café Chain","Tim Hortons":"Café Chain","Country Bean":"Café Chain","Local / Regional Brand":"Local/Regional","Tata Coffee":"Local/Regional","Other":"Other"}
    d["preferred_brand_grouped"]=d["preferredBrand"].astype("string").str.strip().replace(brand_map)
    d["Premium_brand"]=d["preferred_brand_grouped"].isin(["Premium","Café Chain"]).astype(int)
    d["bought_online"]=d["purchaseLocation"].isin(["Online Marketplace"]).astype(int)
    d["Premium_type"]=d["preferredCoffeeType"].isin(["Flavoured / Specialty","Cold Brew"]).astype(int)
    new_features=d.groupby("city")[["Premium_brand","bought_online","Premium_type"]].mean().reset_index()
    return city.merge(new_features,on="city")

def build_city_features(df,external):
    city=_city_base(df).merge(external,on="city",how="inner")
    return city

def cluster_cities(city_df,n_clusters=3,random_state=42):
    X=city_df.drop(columns=["city","cluster","market_type"],errors="ignore")
    X_scaled=StandardScaler().fit_transform(X)
    model=KMeans(n_clusters=n_clusters,random_state=random_state,n_init=10)
    labels=model.fit_predict(X_scaled); out=city_df.copy(); out["cluster"]=labels
    return out,pd.DataFrame([{"Evaluation":"Full city features","Silhouette_Score":silhouette_score(X_scaled,labels)}])

def city_opportunity(city_df):
    out=city_df.copy()
    def mm(s): return (s-s.min())/(s.max()-s.min())
    out["opportunity_score"]=(mm(out["monthlyCoffeeSpend"])+mm(out["cafe_density"])+mm(out["income_index"]))/3
    return out

def score_market_entry(city_df):
    d=city_df.copy()
    def mm(s):
        s=pd.Series(s,dtype=float)
        return pd.Series(.5,index=s.index) if s.max()==s.min() else (s-s.min())/(s.max()-s.min())
    d["adoption_score"]=mm(d.get("adoption_signal",pd.Series(0,index=d.index)).fillna(0))
    d["spending_score"]=mm(d["monthlyCoffeeSpend"])
    d["city_strength_score"]=(mm(d["cafe_density"])+mm(d["income_index"])+mm(d["ecommerce_pct"]))/3
    d["trend_score"]=.5
    d["market_entry_score"]=(d["adoption_score"]+d["spending_score"]+d["city_strength_score"]+d["trend_score"])/4
    d=d.sort_values("market_entry_score",ascending=False).reset_index(drop=True); d["rank"]=np.arange(1,len(d)+1)
    return d

def load_ranking(path="outputs/datasets/market_entry_ranking.csv"): return pd.read_csv(path)
def load_sensitivity(path="outputs/datasets/recommendation_sensitivity.csv"): return pd.read_csv(path)
