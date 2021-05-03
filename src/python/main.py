from pytrends.request import TrendReq
import pandas as pd 
import seaborn as sns
from datetime import datetime,date,timedelta
import time
from tqdm import tqdm

path = '../list.csv'

today = str(date.today())
start_date = str(date.today() - timedelta(7))
end_date = str(date.today())

with open(path,'r') as p:
    file_content = p.read().split(',\n')
final_dict = pd.DataFrame()
related_topic_df = pd.DataFrame()
def get_data(file_content):
    global final_dict 
    global related_topic_df
    
    pytrends = TrendReq(hl='india',tz=360,retries=5,backoff_factor=0.5)

    for search in file_content:
        try:
            pytrends.build_payload(kw_list=[search],timeframe=f"{start_date} {end_date}",geo='IN')
            df = pytrends.interest_over_time().reset_index()
            df.drop(labels=['isPartial'],axis=1,inplace=True)
            final_dict = pd.concat([final_dict , df ],axis=1) 
            related_topic = pytrends.related_topics()[search]['rising'].reset_index()
            related_topic_df = pd.concat([related_topic,related_topic_df],ignore_index=True,axis=1) 
        except Exception as error:
            print(error)

    if related_topic_df.empty: pass
  
    final_dict.to_csv(f'..//..//output/final_df_{today}.csv',index=False)
    related_topic_df.to_csv(f'..//..//output/related_topic_df_{today}.csv',index=False)


get_data(file_content = file_content)



