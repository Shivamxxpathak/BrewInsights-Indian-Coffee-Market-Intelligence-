import pandas as pd
from src.market_entry import build_city_features, score_market_entry, cluster_cities

def test_market_entry_pipeline():
    df=pd.DataFrame({
        "city":["Delhi","Delhi","Mumbai","Mumbai"],
        "monthlyCoffeeSpend":[500,600,400,450],
        "monthlyIncome":[50000,60000,40000,45000],
        "age":[25,30,40,35],
        "purchaseIntention":["Definitely Would Buy","Probably Would Buy","Probably Would Not Buy","Probably Would Buy"],
        "willingnessToTry":["Likely","Very Likely","Unlikely","Neutral"],
        "coffeeFrequency":["Daily","3-4 times/week","Rarely","1-2 times/week"],
        "brandLoyalty":["High","Medium","Low","Medium"],
        "purchaseMode":["Online","Offline","Online","Offline"],
        "priceSensitivity":["Medium"]*4,
        "preferredBrand":["Nescafe"]*4,
        "purchaseLocation":["Online Marketplace"]*4,
        "preferredCoffeeType":["Instant Coffee"]*4
    })
    ext=pd.DataFrame({"city":["Delhi","Mumbai"],"cafe_density":[80,60],"income_index":[100000,80000],"city_tier":[1,1],"competitor_count":[20,25],"ecommerce_pct":[70,60]})
    cities=build_city_features(df,ext); scored=score_market_entry(cities); clustered,metrics=cluster_cities(cities,n_clusters=2)
    assert len(scored)==2 and len(clustered)==2 and metrics["Silhouette_Score"].notna().all()
