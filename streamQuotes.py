import json
import requests
import config

response = requests.post('https://api.tradier.com/v1/markets/events/session',
                         data={},
                         headers={'Authorization': 'Bearer {}'.format(
                             config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'}
                         )

json_response = response.json()

# Directly access 'sessionid' from the nested dictionary
session_id = json_response.get('stream', {}).get('sessionid', 'Default Value')


headers = {
    'Accept': 'application/json'
}
print(session_id)
payload = {
    'sessionid': session_id,
    'symbols': 'qqq',
    'linebreak': True
}

r = requests.get('https://stream.tradier.com/v1/markets/events',
                 stream=True, params=payload, headers=headers)
for line in r.iter_lines():
    if line:
        print(json.loads(line))
