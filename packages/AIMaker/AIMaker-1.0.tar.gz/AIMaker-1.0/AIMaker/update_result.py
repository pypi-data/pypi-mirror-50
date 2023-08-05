import os
import requests
import json

KEY_RESULT_VALUE = "result"

def sendUpdateRequest(c):
    job = os.environ['AI_MAKER_JOB_ID']
    param = os.environ['AI_MAKER_PARAM_ID']
    token = os.environ['AI_MAKER_TOKEN']
    url = os.environ['AI_MAKER_HOST']
    HEADERS = {"content-type" : "application/json",
               "Authorization" : token}
    body = json.dumps({ KEY_RESULT_VALUE : c })
    url = url+"/api/v1/smart-ml/callback/results/jobs/"+job+"/params/"+param
    return requests.post(url, data = body, headers = HEADERS)
