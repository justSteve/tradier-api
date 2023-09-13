import config
import requests
import json
import sys
import pandas as pd


account_id = config.ACCOUNT_ID_pjk
accessToken = config.ACCESS_TOKEN_pjk
response = requests.get("https://api.tradier.com/v1/accounts/{account_id}/history",
    params={},
    headers={"Authorization": "Bearer {accessToken}", "Accept": "application/json"}
)
json_response = response.json()
print(response.status_code)
print(json_response)
print(account_id)
print(accessToken)