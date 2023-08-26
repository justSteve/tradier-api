#I don't get the point of this api unless there's more filters than just underlying. 
import config
import requests
import json
import sys
import pandas as pd


url = "{}markets/options/lookup".format(config.API_BASE_URL)

headers = {
    'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN),
    'Accept': 'application/json'
}
response = requests.get(url,
                        params={'underlying': 'spx', },
                        
                        headers=headers
                        )

# Check if the request was successful
if response.status_code == 200:


    json_response = response.json()
    print(response.status_code)
    print(json_response)
else:
    print('Error with the request:', response.status_code, response.text)

# json_response = response.json()
# print(response.status_code)
# print(json_response)
