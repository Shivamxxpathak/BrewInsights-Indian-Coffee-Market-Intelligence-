"""New-brand adoption modeling utilities."""
from __future__ import annotations
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.tree import DecisionTreeClassifier

TARGET_MAP={"Probably Would Buy":1,"Definitely Would Buy":1,"Probably Would Not Buy":0,"Definitely Would Not Buy":0}

def make_adoption_target(df,column="purchaseIntention"):
    if column not in df: raise ValueError(f"Missing target column: {column}")
    return df[column].map(TARGET_MAP).fillna(df[column].astype("string").str.lower().map({k.lower():v for k,v in TARGET_MAP.items()}))

def train_adoption_models(df,random_state=42):
    y=make_adoption_target(df); mask=y.notna(); data=df.loc[mask].copy(); y=y.loc[mask].astype(int)
    drop=[c for c in ["purchaseIntention","respondentId","email","createdAt","source"] if c in data]; X=data.drop(columns=drop)
    numeric=X.select_dtypes(include=["number"]).columns.tolist(); categorical=X.select_dtypes(exclude=["number"]).columns.tolist()
    pre=ColumnTransformer([("num",Pipeline([("scale",StandardScaler())]),numeric),("cat",OneHotEncoder(handle_unknown="ignore"),categorical)])
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,stratify=y,random_state=random_state)
    models={"Logistic Regression":LogisticRegression(max_iter=2000,random_state=random_state),"Decision Tree":DecisionTreeClassifier(max_depth=6,random_state=random_state),"Random Forest":RandomForestClassifier(n_estimators=300,random_state=random_state,class_weight="balanced"),"Gradient Boosting":GradientBoostingClassifier(random_state=random_state)}
    rows=[]; fitted={}
    for name,estimator in models.items():
        pipe=Pipeline([("preprocess",pre),("model",estimator)]); pipe.fit(X_train,y_train); pred=pipe.predict(X_test); proba=pipe.predict_proba(X_test)[:,1]
        rows.append({"Model":name,"Accuracy":accuracy_score(y_test,pred),"Precision":precision_score(y_test,pred,zero_division=0),"Recall":recall_score(y_test,pred,zero_division=0),"F1":f1_score(y_test,pred,zero_division=0),"ROC_AUC":roc_auc_score(y_test,proba)}); fitted[name]=pipe
    return pd.DataFrame(rows),fitted

def load_results(path="outputs/datasets/adoption_model_comparison.csv"): return pd.read_csv(path)
