"""Notebook-parity new-brand adoption modeling utilities."""
from __future__ import annotations
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import xgboost as xgb

def _prepare(df):
    out=df.copy()
    out["willingnessToTry"]=out["willingnessToTry"].replace({
        "Likely":1,"Very Likely":1,"Unlikely":0,"Very Unlikely":0,
        "Somewhat willing":1,"Very willing":1,"Not currently interested":0,
        "Only with a recommendation":0,"Neutral":0
    })
    for c,m in {
        "coffeeFrequency":{"Rarely":0,"few":0,"rarely":0,"1-2 times/week":1,"sometimes":1,"3-4 times/week":2,"Daily":3,"daily":3,"Multiple times/day":4},
        "brandLoyalty":{"Low":0,"No Preference":0,"Medium":1,"Somewhat Loyal":1,"High":2,"Very Loyal":2,"I Like To Explore":0},
        "purchaseIntention":{"High":1,"Definitely would buy":1,"Low":0,"Not sure":0,"Probably would buy":2,"Medium":2},
        "purchaseMode":{"Online":1,"Mostly online":1,"Offline":0,"Mostly offline":0,"Both equally":2,"Both":2}
    }.items():
        if c in out: out[c]=out[c].map(m)
    if "city" in out:
        out["city"]=out["city"].replace({"delhi":"Delhi","New delhi":"Delhi","New Delhi":"Delhi","noida":"Noida","Greater noida":"Noida"})
    if "occupation" in out:
        out["occupation"]=out["occupation"].replace({"Teacher":"Teacher/Professor","Business":"Business Owner","Engineering Student":"Student","Farmer":"Other","Employee":"IT Professional","Engineer":"IT Professional","Designer":"Other","DESIGNER":"Other","Buisness":"Business Owner","Communication Professional":"Other","Nurse":"Healthcare Professional","On Bed":"Other","HR":"Other","Private employee":"IT Professional","Sutdent":"Student","Trainer":"Other","employee":"Other","student":"Student"})
    out=out.drop(columns=["preferredCoffeeType","gender","purchaseIntention"],errors="ignore")
    out=pd.get_dummies(out,columns=[c for c in ["priceSensitivity","tastePreference","purchaseLocation","preferredBrand"] if c in out],dtype=int)
    out=out.dropna().astype(int)
    return out

def train_adoption_models(df,random_state=0):
    data=_prepare(df)
    if "willingnessToTry" not in data: raise ValueError("Missing willingnessToTry target.")
    X=data.drop(columns=["willingnessToTry"]); y=data["willingnessToTry"].astype(int)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,random_state=random_state)
    models={
        "Logistic Regression":LogisticRegression(max_iter=1000),
        "Decision Tree":DecisionTreeClassifier(random_state=random_state),
        "Random Forest":RandomForestClassifier(n_estimators=100,random_state=random_state),
        "XGBoost":xgb.XGBClassifier(n_estimators=100,learning_rate=.1,random_state=random_state),
        "Gradient Boosting":GradientBoostingClassifier(n_estimators=200,learning_rate=.05,max_depth=3,random_state=42)
    }
    rows=[]; fitted={}
    for name,model in models.items():
        model.fit(X_train,y_train); pred=model.predict(X_test); proba=model.predict_proba(X_test)[:,1]
        row={"Model":name,"Accuracy":accuracy_score(y_test,pred)}
        if name in {"Logistic Regression","Random Forest","Gradient Boosting"}:
            row.update({"Precision":precision_score(y_test,pred),"Recall":recall_score(y_test,pred),"F1":f1_score(y_test,pred),"ROC_AUC":roc_auc_score(y_test,proba)})
        rows.append(row); fitted[name]=model
    return pd.DataFrame(rows),fitted

def load_results(path="outputs/datasets/adoption_model_comparison.csv"): return pd.read_csv(path)
