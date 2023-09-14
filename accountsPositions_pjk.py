
import config
import requests
import json
import sys
import pandas as pd
import re

def parse_iso_string(iso_string):
    # Use regular expression to find groups of alphabetical and numerical characters
    parts = re.findall(r'[A-Za-z]+|\d+', iso_string)
    
    if len(parts) != 4:
        return "Invalid ISO String"

    symbol, expiry, optionType, strike = parts
    return symbol, expiry, optionType, int(strike)


account_id = config.ACCOUNT_ID_pjk
accessToken = config.ACCESS_TOKEN_pjk


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

print(json_response)




