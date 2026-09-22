"""Coffee-spending regression utilities."""
from __future__ import annotations
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

TARGET="monthlyCoffeeSpend"

def train_spending_model(df,random_state=42):
    if TARGET not in df: raise ValueError(f"Missing target column: {TARGET}")
    data=df.dropna(subset=[TARGET]).copy(); y=pd.to_numeric(data[TARGET],errors="coerce"); mask=y.notna(); data=data.loc[mask]; y=y.loc[mask]
    drop=[c for c in [TARGET,"respondentId","email","createdAt","source"] if c in data]; X=data.drop(columns=drop)
    numeric=X.select_dtypes(include=["number"]).columns.tolist(); categorical=X.select_dtypes(exclude=["number"]).columns.tolist()
    pre=ColumnTransformer([("num",StandardScaler(),numeric),("cat",OneHotEncoder(handle_unknown="ignore"),categorical)])
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,random_state=random_state)
    pipe=Pipeline([("preprocess",pre),("model",LinearRegression())]); pipe.fit(X_train,y_train); pred=pipe.predict(X_test)
    metrics=pd.DataFrame([{"Model":"Linear Regression","MAE":mean_absolute_error(y_test,pred),"RMSE":mean_squared_error(y_test,pred)**.5,"R2":r2_score(y_test,pred)}])
    return metrics,pipe

def load_results(path="outputs/datasets/spending_model_comparison.csv"): return pd.read_csv(path)
