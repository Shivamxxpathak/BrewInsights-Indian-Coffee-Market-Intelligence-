import pandas as pd
from src.demand_forecasting import build_demand_series, forecast_demand
def test_demand_forecast_shapes():
    df=pd.DataFrame({"coffeeFrequency":["Often"]*48,"purchaseIntention":["Probably Would Buy"]*48,"monthlyCoffeeSpend":[500+i for i in range(48)]})
    s=build_demand_series(df); f,m=forecast_demand(s,horizon=6); assert len(s)==24 and len(f)==18 and len(m)==3
