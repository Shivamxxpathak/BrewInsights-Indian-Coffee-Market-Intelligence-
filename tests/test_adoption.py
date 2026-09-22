import pandas as pd
from src.adoption_prediction import make_adoption_target
def test_adoption_target_mapping():
    assert make_adoption_target(pd.DataFrame({"purchaseIntention":["Definitely Would Buy","Probably Would Not Buy"]})).tolist()==[1,0]
