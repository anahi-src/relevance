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
    e = enki.Enki(api_key=settings.api_key, endpoint=settings.endpoint, project_short_name=kwargs['project_short_name'], all=1)
    e.get_tasks(task_id=kwargs['task_id'])
    post_id = e.tasks_df['_id'][kwargs['task_id']]
    e.get_task_runs()
    df = e.task_runs_df[kwargs['task_id']]
    total = len(df[df.columns[0]])
    subset = df[df.columns[0]].apply(pd.Series)[0].apply(pd.Series)
    trueCount = len(subset[subset[subset.columns[0]]==True])
    relevance = trueCount/total
    payload = {
        "name":"relevance",
        "post":post_id,
        "value":str(relevance)
        }
    user = # e2mc data api username. Although harcoded here, it could be easily included in the settings file
    pass = # e2mc data api password. Although harcoded here, it could be easily included in the settings file
    r = requests.post('http://131.175.120.92:5555/e2mc/datapi/v1.1/tags', auth=(user, pass), headers=headers, data=json.dumps(payload))
    with open('./static/results.json', 'w') as f:
        f.write(json.dumps(kwargs))
    return r
