from logging import exception
import pandas as pd 
import time 
import os, sys 
import requests
import datetime
import fake_useragent
import json

today = datetime.datetime.today() - datetime.timedelta(days=7)
week_day = today.weekday()
week_back = today - datetime.timedelta(days=week_day )
week_start = datetime.datetime.strftime(week_back,'%Y%m%d')
week_end = datetime.datetime.strftime(week_back + datetime.timedelta(days=6),'%Y%m%d')
week_ending_date = str(week_back + datetime.timedelta(days=6)).split(' ')[0]
output_dir = f'../../Output_shows/{week_ending_date }'

try:
    os.mkdir(f'../../Output_shows/{week_ending_date }')
except:
    print('dir exists')


shows = pd.read_csv('../../Input_disney_shows/comedy_drama_series.csv')


type = 'en'
agent = 'user'
granularity = 'daily'
platform = ('mobile-web','desktop','mobile-app')
api = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'
article = 'The_Adventures_of_Ozzie_and_Harriet'
project = 'en.wikipedia.org'
access = 'desktop'
params = f'{project}/{access}/{agent}/{article}/{granularity}/{week_start}/{week_end}'


headers = {

 'accept-ranges': 'bytes',
 'access-control-allow-headers': 'accept,content-type,content-length,cache-control,accept-language,api-user-agent,if-match,if-modified-since,if-none-match,dnt,accept-encoding', 
 'access-control-allow-methods': 'GET,HEAD' ,
 'access-control-allow-origin': '*',
 'access-control-expose-headers': 'etag' ,
 'age': '0' ,
 'cache-control': 's-maxage=14400,max-age=14400' ,
 'content-encoding': 'gzip' ,
 'content-security-policy': "default-src 'none'; frame-ancestors 'none'",
 'content-type': 'application/json; charset=utf-8',
 'nel': '{ "report_to": "wm_nel","max_age": 86400,"failure_fraction": 0.05,"success_fraction": 0.0}',
 'permissions-policy': 'interest-cohort=()' ,
 'referrer-policy': 'origin-when-cross-origin' ,
 'report-to': '{ "group": "wm_nel","max_age": 86400,"endpoints": [{ "url": "https://intake-logging.wikimedia.org/v1/events?stream=w3c.reportingapi.network_error&schema_uri=/w3c/reportingapi/network_error/1.0.0" }] } ',
 'server': 'restbase2023' ,
 'server-timing': 'cache;desc="miss",host;desc="cp5007" ',
 'strict-transport-security':"max-age=106384710; includeSubDomains; preload ",
 'vary': "Accept-Encoding ",
 'x-cache': "cp5010 miss,cp5007 miss" ,
 'x-cache-status': "miss" ,
 'x-content-security-policy': "default-src 'none'; frame-ancestors 'none'" ,
 'x-content-type-options': "nosniff" ,
 'x-frame-options': "SAMEORIGIN" ,
 'x-webkit-csp': "default-src 'none'; frame-ancestors 'none'" ,
 'x-xss-protection': '1; mode=block ',
 'user-agent': str(fake_useragent.UserAgent().random)



}

data_not_processed = {}
data = []
for r,show in enumerate(shows.values):
    for access in platform:
        article = show[1]
        params = f'{project}/{access}/{agent}/{article}/{granularity}/{week_start}/{week_end}'
        responce = requests.get(api + params ,headers=headers)
        json_data = responce.json()
        try:
            data_list = json_data['items']
            for r in range(len(data_list)): data_list[r].update({'week_ending_date':week_ending_date,'show':show[0]})
            data.extend(data_list)
        except Exception as e:   
            data_not_processed[article + '_' + access] = str(e)
            continue 


df_shows = pd.DataFrame(data)

df_shows.to_csv(f'{output_dir}/shows_{week_ending_date}.csv',index=False)

with open(f'{output_dir}/shows_failed_{week_ending_date}.json','w') as w:
    json.dump(data_not_processed,w)