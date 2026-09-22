import pandas as pd
from src.adoption_prediction import train_adoption_models

def test_adoption_models_include_xgboost():
    df=pd.DataFrame({
        "willingnessToTry":["Likely","Unlikely","Very Likely","Neutral"]*10,
        "coffeeFrequency":["Daily","Rarely","3-4 times/week","1-2 times/week"]*10,
        "brandLoyalty":["High","Low","Medium","Very Loyal"]*10,
        "purchaseIntention":["High","Low","Medium","Definitely would buy"]*10,
        "purchaseMode":["Online","Offline","Both","Online"]*10,
        "age":[20+i%10 for i in range(40)],
        "monthlyIncome":[30000+i*100 for i in range(40)],
        "monthlyCoffeeSpend":[500+i for i in range(40)],
        "preferredPriceRange":["₹201–350"]*40,
        "priceSensitivity":["Medium"]*40,
        "tastePreference":["Balanced"]*40,
        "purchaseLocation":["Online Marketplace"]*40,
        "preferredBrand":["Nescafe"]*40,
        "city":["Delhi"]*40,
        "occupation":["Student"]*40
    })
    results,_=train_adoption_models(df)
    assert "XGBoost" in results["Model"].tolist()
