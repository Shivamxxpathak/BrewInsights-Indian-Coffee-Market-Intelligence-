import pandas as pd
from src.spending_prediction import train_spending_model
def test_spending_model():
    df=pd.DataFrame({"monthlyCoffeeSpend":[100,120,140,160,180,200,220,240,260,280],"age":range(10),"monthlyIncome":[1000+i*100 for i in range(10)],"city":["Delhi","Mumbai"]*5})
    metrics,_=train_spending_model(df); assert metrics.shape==(1,4) and metrics["MAE"].notna().all()
