"""Notebook-parity survey-derived demand trend and forecasting utilities."""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

FREQUENCY={"Rarely":1,"1-2 times/week":2,"3-4 times/week":3,"Daily":4,"Multiple times/day":5}
INTENTION={"Low":1,"Medium":2,"High":3}
PRICE={"Somewhat sensitive":1,"Neutral":2,"Not sensitive at all":3}
LOYALTY={"Very loyal":3,"Somewhat loyal":2,"I like to explore":1}

def build_demand_series(df,periods=24):
    out=df.copy()
    for c,m in [("coffeeFrequency",FREQUENCY),("purchaseIntention",INTENTION),("priceSensitivity",PRICE),("brandLoyalty",LOYALTY)]:
        out[c+"_score"]=out[c].map(m)
        out[c+"_score"]=pd.to_numeric(out[c+"_score"],errors="coerce").fillna(out[c+"_score"].median())
    out["monthlyCoffeeSpend"]=pd.to_numeric(out["monthlyCoffeeSpend"],errors="coerce")
    out["monthlyCoffeeSpend"]=out["monthlyCoffeeSpend"].fillna(out["monthlyCoffeeSpend"].median())
    out["Demand_Score"]=.40*out["coffeeFrequency_score"]+.30*out["purchaseIntention_score"]+.30*(out["monthlyCoffeeSpend"]/out["monthlyCoffeeSpend"].max()*3)
    out=out.reset_index(drop=True)
    out["Period"]=pd.qcut(np.arange(len(out)),q=periods,labels=False)+1
    result=out.groupby("Period")["Demand_Score"].mean().reset_index().rename(columns={"Demand_Score":"Demand"})
    result["Moving_Average"]=result["Demand"].rolling(3).mean()
    return result

def forecast_demand(series,horizon=6):
    X=series[["Period"]]; y=series["Demand"]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.20,random_state=42)
    models={
        "Linear Regression":LinearRegression(),
        "Random Forest":RandomForestRegressor(n_estimators=300,random_state=42),
        "Gradient Boosting":GradientBoostingRegressor(n_estimators=200,learning_rate=.05,max_depth=2,random_state=42)
    }
    rows=[]; fitted={}; future=np.arange(int(series["Period"].max())+1,int(series["Period"].max())+horizon+1); forecasts=[]
    for name,model in models.items():
        model.fit(X_train,y_train); pred=model.predict(X_test)
        rows.append({"Model":name,"MAE":mean_absolute_error(y_test,pred),"RMSE":np.sqrt(mean_squared_error(y_test,pred)),"R2":r2_score(y_test,pred)})
        model.fit(X,y); forecasts.append(pd.DataFrame({"Model":name,"Future_Period":future,"Forecasted_Demand":model.predict(pd.DataFrame({"Period":future}))})); fitted[name]=model
    return pd.concat(forecasts,ignore_index=True),pd.DataFrame(rows),fitted

def load_demand(path="data/coffee_demand_by_period.csv"): return pd.read_csv(path)
def load_forecast(path="data/coffee_demand_forecast.csv"): return pd.read_csv(path)
def load_model_comparison(path="data/coffee_demand_model_comparison.csv"): return pd.read_csv(path)
