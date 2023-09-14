import config
import requests
import json
import sys
import pandas as pd


account_id = config.ACCOUNT_ID_pjk
accessToken = config.ACCESS_TOKEN_pjk
response = requests.get("https://api.tradier.com/v1/accounts/" + account_id + "/gainloss",
    params={"page": "3", "limit": "100", "sortBy": "closeDate", "sort": "desc", "start": "yyyy-MM-dd", "end": "yyyy-MM-dd", "symbol": "SPX"},
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