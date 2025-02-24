import pandas as pd
import json
from typing import List
from agent import NewsletterWriterAgent
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


