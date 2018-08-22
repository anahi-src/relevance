from __future__ import division
import enki
import pandas as pd
import json
import settings
import requests

def relevance(**kwargs):
    headers = {
        'Content-Type': 'application/json',
        }
    
    # Obtain task run results from Pybossa:
    e = enki.Enki(api_key=settings.api_key, endpoint=settings.endpoint, project_short_name=kwargs['project_short_name'], all=1)
    e.get_tasks(task_id=kwargs['task_id'])
    post_id = e.tasks_df['_id'][kwargs['task_id']]
    e.get_task_runs()
    df = e.task_runs_df[kwargs['task_id']]
    
    # Calculate total number of answers for the task and create a subset DF:
    total = len(df[df.columns[0]])
    subset = df[df.columns[0]].apply(pd.Series)[0].apply(pd.Series)
    
    # Count the number of times the image was considered relevant:
    trueCount = len(subset[subset[subset.columns[0]]==True])
    
    # Calculate relevance:
    relevance = trueCount/total
    
    #Prepare payload:
    payload = {
        "name":"relevance",
        "post":post_id,
        "value":str(relevance)
        }
    
    # e2mc data API credentials:
    username = # e2mc data api username. Although harcoded here, it could be easily included in the settings file
    password = # e2mc data api password. Although harcoded here, it could be easily included in the settings file
    
    # Push payload into data API
    r = requests.post('http://131.175.120.92:5555/e2mc/datapi/v1.1/tags', auth=(username, password), headers=headers, data=json.dumps(payload))
    
    # Create record file:
    with open('./static/results.json', 'w') as f:
        f.write(json.dumps(kwargs))
    return r
