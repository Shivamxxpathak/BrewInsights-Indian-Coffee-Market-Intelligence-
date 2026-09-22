import pandas as pd
from src.demand_forecasting import build_demand_series, forecast_demand

def test_demand_forecast_shapes():
    df=pd.DataFrame({"coffeeFrequency":["Daily"]*48,"purchaseIntention":["High"]*48,"monthlyCoffeeSpend":[500+i for i in range(48)],"priceSensitivity":["Neutral"]*48,"brandLoyalty":["Medium"]*48})
    s=build_demand_series(df); f,m,_=forecast_demand(s,horizon=6)
    assert len(s)==24 and len(f)==18 and len(m)==3
