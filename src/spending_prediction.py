"""Notebook-parity coffee-spending regression utilities."""
from __future__ import annotations
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error

def _prepare(df):
    out=df.copy()
    income_map={"Below ₹25,000":12500,"₹25,000–₹50,000":37500,"₹50,000–₹1,00,000":75000,"Above ₹1,00,000":125000}
    spend_map={"Under ₹500":490,"₹500–₹1,000":700,"₹1,000–₹2,500":2400,"Above ₹2,500":4000}
    price_map={"₹50–100":90,"₹101–200":130,"Under ₹200":150,"₹201–350":300,"₹351–500":450,"₹200–₹500":400,"₹500–₹1,000":950,"₹500+":700,"Above ₹1,000":2000}
    for c,m in [("monthlyIncome",income_map),("monthlyCoffeeSpend",spend_map),("preferredPriceRange",price_map)]:
        if c in out:
            out[c]=out[c].map(m).fillna(pd.to_numeric(out[c],errors="coerce"))
    for c,m in {
        "coffeeFrequency":{"Rarely":0,"few":0,"rarely":0,"1-2 times/week":1,"sometimes":1,"3-4 times/week":2,"Daily":3,"daily":3,"Multiple times/day":4},
        "brandLoyalty":{"Low":0,"No Preference":0,"Medium":1,"Somewhat Loyal":1,"High":2,"Very Loyal":2,"I Like To Explore":0},
        "purchaseIntention":{"High":1,"Definitely would buy":1,"Low":0,"Not sure":0,"Probably would buy":2,"Medium":2},
        "purchaseMode":{"Online":1,"Mostly online":1,"Offline":0,"Mostly offline":0,"Both equally":2,"Both":2},
        "willingnessToTry":{"Likely":1,"Very Likely":1,"Unlikely":0,"Very Unlikely":0,"Somewhat willing":1,"Very willing":1,"Not currently interested":0,"Only with a recommendation":0,"Neutral":0}
    }.items():
        if c in out: out[c]=out[c].map(m)
    out=out.drop(columns=["preferredCoffeeType","gender"],errors="ignore")
    out=out.rename(columns={"age":"Age","monthlyIncome":"Income","monthlyCoffeeSpend":"Coffee_Spend","preferredBrand":"Current_Brand","priceSensitivity":"Price_Sensitivity","tastePreference":"Premium_Preference","purchaseLocation":"Product_Format","willingnessToTry":"Will_Buy_New_Brand"})
    for c in ["gender","city","occupation","preferredCoffeeType","preferredBrand","purchaseLocation","purchaseMode","priceSensitivity","tastePreference","brandLoyalty","willingnessToTry","purchaseIntention"]:
        if c in out: out[c]=out[c].fillna(out[c].mode()[0])
    out=pd.get_dummies(out,columns=[c for c in ["Price_Sensitivity","Premium_Preference","Product_Format","Current_Brand"] if c in out])
    out=out.dropna()
    return out

def train_spending_model(df,random_state=42):
    data=_prepare(df); X=data.drop(columns=["Coffee_Spend"]); y=data["Coffee_Spend"]
    categorical_features=X.select_dtypes(include=["object","category"]).columns
    numerical_features=X.select_dtypes(include=["int64","float64"]).columns
    categorical_pipeline=Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("encoder",OneHotEncoder(handle_unknown="ignore"))])
    numerical_pipeline=Pipeline([("imputer",SimpleImputer(strategy="median"))])
    preprocessor=ColumnTransformer([("categorical",categorical_pipeline,categorical_features),("numerical",numerical_pipeline,numerical_features)])
    model=Pipeline([("preprocessor",preprocessor),("regressor",LinearRegression())])
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,random_state=random_state)
    model.fit(X_train,y_train); pred=model.predict(X_test)
    return pd.DataFrame([{"Model":"Linear Regression","MAE":mean_absolute_error(y_test,pred),"RMSE":np.sqrt(mean_squared_error(y_test,pred)),"R2":r2_score(y_test,pred)}]),model

def load_results(path="outputs/datasets/spending_model_comparison.csv"): return pd.read_csv(path)
