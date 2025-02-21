import pandas as pd
import json
from typing import List
def make_table(processed_events:List):
    formatted_events=[]
    for event in processed_events:
        df_dict={}
        event_details=event.get("details", None)
        if event_details is not None:
            df_dict={**event_details}
        df_dict['url']=event['detail_link']
        df_dict['title']=event['title']
        formatted_events.append(df_dict)
    df=pd.DataFrame(formatted_events)
    return df

with open("final_output.json", "r") as f:
    processed_events=json.loads(f.read())

formatted_events=make_table(processed_events)
formatted_events.to_csv("n19qz.csv")