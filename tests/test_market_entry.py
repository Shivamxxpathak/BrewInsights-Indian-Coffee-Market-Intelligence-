import pandas as pd
from src.market_entry import build_city_features, score_market_entry, cluster_cities
def test_market_entry_pipeline():
    df=pd.DataFrame({"city":["Delhi","Delhi","Mumbai","Mumbai"],"monthlyCoffeeSpend":[500,600,400,450],"monthlyIncome":[50000,60000,40000,45000],"purchaseIntention":["Definitely Would Buy","Probably Would Buy","Probably Would Not Buy","Probably Would Buy"]})
    ext=pd.DataFrame({"city":["Delhi","Mumbai"],"cafe_density":[80,60],"income_index":[100000,80000],"city_tier":[1,1]}); cities=build_city_features(df,ext); scored=score_market_entry(cities); clustered,metrics=cluster_cities(cities,n_clusters=2); assert len(scored)==2 and len(clustered)==2 and metrics["silhouette_score"].notna().all()
