import config
import requests
import json
import sys
import pandas as pd


account_id = config.ACCOUNT_ID_sjh
accessToken = config.ACCESS_TOKEN_sjh
response = requests.get("https://api.tradier.com/v1/accounts/" + account_id + "/positions",
    params={},
    headers={"Authorization": "Bearer " + accessToken, "Accept": "application/json"}
)
try:
    json_response = response.json()
except Exception as e:
    print ("exception hit!!")
    print (e)
    print(response)
    print(response.text)
    sys.exit(1)
    
print(response.status_code)
print(json_response)
print(account_id)
print(accessToken)