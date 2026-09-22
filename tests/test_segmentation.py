import pandas as pd
from src.segmentation import segment_consumers
def test_segment_consumers_returns_labels():
    df=pd.DataFrame({"age":range(12),"monthlyIncome":[10000+i*1000 for i in range(12)],"monthlyCoffeeSpend":[100+i*20 for i in range(12)],"preferredPriceRange":[100+i*10 for i in range(12)]})
    a,p,m=segment_consumers(df,n_clusters=3); assert len(a)==12 and len(p)==3 and m["silhouette_score"].notna().all()
