import pandas as pd
from src.data_cleaning import clean_dataframe
def test_cleaning_removes_identifiers_and_duplicates():
    out=clean_dataframe(pd.DataFrame({"respondentId":[1,1],"email":["a","a"],"age":["22","22"],"city":[" Delhi "," Delhi "]}))
    assert "email" not in out.columns and len(out)==1 and out.loc[0,"age"]==22
