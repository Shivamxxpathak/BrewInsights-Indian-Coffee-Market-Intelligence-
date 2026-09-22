"""Executable BrewInsights reproducibility runner.

Writes validation outputs to outputs/pipeline_validation without overwriting
canonical notebook artifacts.
"""
from pathlib import Path
import json,sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.data_cleaning import clean_dataframe,validate_required_columns
from src.segmentation import segment_consumers,compare_clustering
from src.adoption_prediction import train_adoption_models
from src.spending_prediction import train_spending_model
from src.demand_forecasting import build_demand_series,forecast_demand
from src.market_entry import build_city_features,score_market_entry,cluster_cities

def main():
    data=ROOT/"data/processed/coffee_cleaned.csv"; external=ROOT/"data/external_city_data.csv"; out=ROOT/"outputs/pipeline_validation"; out.mkdir(parents=True,exist_ok=True)
    df=clean_dataframe(pd.read_csv(data)); validate_required_columns(df,["city","age","monthlyIncome","monthlyCoffeeSpend","preferredPriceRange","purchaseIntention"])
    a,p,m=segment_consumers(df); a.to_csv(out/"consumer_cluster_assignments.csv",index=False); p.to_csv(out/"consumer_cluster_profiles.csv",index=False); m.to_csv(out/"consumer_clustering_metrics.csv",index=False); compare_clustering(df).to_csv(out/"clustering_method_comparison.csv",index=False)
    adoption,_=train_adoption_models(df); adoption.to_csv(out/"adoption_model_comparison.csv",index=False)
    spending,_=train_spending_model(df); spending.to_csv(out/"spending_model_comparison.csv",index=False)
    demand=build_demand_series(df); forecasts,dm,_=forecast_demand(demand)
best=dm.sort_values("R2",ascending=False).iloc[0]["Model"]
best_forecast=forecasts[forecasts["Model"]==best].rename(columns={"Future_Period":"Future_Period","Forecasted_Demand":"Forecasted_Demand"})[["Future_Period","Forecasted_Demand"]]
demand.to_csv(out/"demand_by_period.csv",index=False); best_forecast.to_csv(out/"demand_forecast.csv",index=False); dm.to_csv(out/"demand_model_comparison.csv",index=False)
    cities=build_city_features(df,pd.read_csv(external))
scored=score_market_entry(cities); scored.to_csv(out/"market_entry_validation.csv",index=False)
clustered,cm=cluster_cities(cities)
X_no_tier=clustered.drop(columns=["city","city_tier","cluster","market_type"],errors="ignore")
if len(X_no_tier)>=3:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    xs=StandardScaler().fit_transform(X_no_tier)
    km=KMeans(n_clusters=3,random_state=42,n_init=10).fit(xs)
    cm=pd.concat([cm,pd.DataFrame([{"Evaluation":"Without city tier","Silhouette_Score":silhouette_score(xs,km.labels_)}])],ignore_index=True)
clustered.to_csv(out/"city_cluster_validation.csv",index=False); cm.to_csv(out/"city_clustering_metrics.csv",index=False)
    summary={"status":"completed","rows":len(df),"columns":len(df.columns),"cities":int(cities.city.nunique()),"adoption_models":len(adoption)}; (out/"run_summary.json").write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
