import pandas as pd
import requests
import time
import sys
import json

def score(df, url):
    df = df.fillna('')
    rows = df.astype(str).to_dict(orient='split')
    rows.pop('index')
    rows['fields'] = rows.pop('columns')
    rows['rows'] = rows.pop('data')
    return requests.post(url, json=eval(str(rows)))

def res_to_df(response):
    rows = json.loads(response.text)
    rows.pop('id')
    rows['columns'] = rows.pop('fields')
    rows['data'] = rows.pop('score')
    return pd.read_json(json.dumps(rows), orient='split')

def get_prediction(df, url):
    pred = res_to_df(score(df, url))
    return pred.iloc[:,1]
