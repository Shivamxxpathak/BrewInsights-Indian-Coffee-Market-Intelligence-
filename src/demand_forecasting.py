"""Survey-derived demand trend construction and forecasting."""
from __future__ import annotations
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

FREQ={"Never":0,"Rarely":1,"Sometimes":2,"Often":3,"Daily":4}; INTENT={"Definitely Would Not Buy":0,"Probably Would Not Buy":1,"Probably Would Buy":2,"Definitely Would Buy":3}

def build_demand_series(df,periods=24):
    freq=df.get("coffeeFrequency",pd.Series(index=df.index,dtype="object")).map(FREQ).fillna(pd.to_numeric(df.get("coffeeFrequency"),errors="coerce"))
    intent=df.get("purchaseIntention",pd.Series(index=df.index,dtype="object")).map(INTENT).fillna(pd.to_numeric(df.get("purchaseIntention"),errors="coerce"))
    spend=pd.to_numeric(df.get("monthlyCoffeeSpend"),errors="coerce"); demand=pd.concat([freq,intent,spend.rank(pct=True)],axis=1).mean(axis=1).dropna().reset_index(drop=True)
    demand.index=(demand.index%periods)+1; out=demand.groupby(level=0).mean().rename("Demand").reset_index().rename(columns={"index":"Period"}); out["Moving_Average"]=out["Demand"].rolling(3).mean(); return out

def forecast_demand(series,horizon=6):
    y=series["Demand"].astype(float).to_numpy(); t=range(1,len(y)+1); future=range(len(y)+1,len(y)+horizon+1)
    factories={"Linear Regression":LinearRegression,"Random Forest":lambda:RandomForestRegressor(n_estimators=300,random_state=42),"Gradient Boosting":lambda:GradientBoostingRegressor(random_state=42)}; forecasts=[]; comparison=[]
    split=max(3,int(len(y)*.8)); X=list(t)
    for name,factory in factories.items():
        model=factory(); model.fit([[v] for v in X[:split]],y[:split]); pv=model.predict([[v] for v in X[split:]]); comparison.append({"Model":name,"MAE":mean_absolute_error(y[split:],pv),"RMSE":mean_squared_error(y[split:],pv)**.5,"R2":r2_score(y[split:],pv)})
        model.fit([[v] for v in X],y); forecasts.append(pd.DataFrame({"Model":name,"Period":list(future),"Forecast":model.predict([[v] for v in future])}))
    return pd.concat(forecasts,ignore_index=True),pd.DataFrame(comparison)

def load_demand(path="data/coffee_demand_by_period.csv"): return pd.read_csv(path)
def load_forecast(path="data/coffee_demand_forecast.csv"): return pd.read_csv(path)
def load_model_comparison(path="data/coffee_demand_model_comparison.csv"): return pd.read_csv(path)
