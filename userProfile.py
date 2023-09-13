import config
import requests
import json
import sys
import pandas as pd

accessToken = config.ACCESS_TOKEN_pjk
response = requests.get("https://api.tradier.com/v1/user/profile",
                        headers={"Authorization": "Bearer {accessToken}", "Accept": "application/json"}
                        )
json_response = response.json()
print(response.status_code)
print(json_response)
print(accessToken)
