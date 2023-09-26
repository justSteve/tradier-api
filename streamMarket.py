import asyncio
import websockets
import config
import requests
import json
import sys



response = requests.post('https://api.tradier.com/v1/accounts/events/session',
                            data={},
                            headers={'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'})
json_response = response.json()
# Directly access 'sessionid' from the nested dictionary
session_id = json_response.get('stream', {}).get(
    'sessionid', 'Default Value')
print("my sessionid = " + session_id)



headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk)
}

payload = { 
  #'sessionid': session_id,
  'sessionid': '585f3c19-287f-4fce-a91d-5001f1b7ecf7',
  'symbols': 'SPY',
  'linebreak': True
}


r = requests.post('https://stream.tradier.com/v1/markets/events', stream=True, params=payload, headers=headers)
for line in r.iter_lines():
    if line:
        try:
            data = json.loads(line)
            print(data)
        except json.JSONDecodeError:
            print(f"Unable to decode line: {line}")