import requests
import config

response = requests.post('https://api.tradier.com/v1/markets/events/session',
                         data={},
                         headers={'Authorization': 'Bearer {}'.format(
                             config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'}
                         )
json_response = response.json()
print(response.status_code)
print(json_response)
