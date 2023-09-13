import config
import requests
import json
import sys
import pandas as pd


gexURL = "http://api.gexbot.com/spx/zero/gex?key=" + config.API_GEXBOT_KEY

gexURL = config.API_URL_GEXBOT + config.API_GEXBOT_KEY
# gexURL = ".format(config.API_GEXBOT_URL).format(config.API_GEXBOT_KEY)"
responseGex = requests.get(gexURL)


json_response = responseGex.json()
print(responseGex.status_code)
print(gexURL)
print(json_response)


url = "{}markets/quotes".format(config.API_BASE_URL)

headers = {
    'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN),
    'Accept': 'application/json'
}
response = requests.get(url,
                        # params={'symbol': 'spx', 'expiration': '2023-09-06', 'greeks': 'true'},
                        params={'symbols': 'SPX231215C04545000',
                                'greeks': 'true'},
                        # params={'symbol': sys.argv[1], 'expiration': sys.argv[2], 'greeks': 'true'},
                        headers=headers
                        )

# Check if the request was successful
if response.status_code == 200:

    # Extract the strikes
    # data = response.json()

    # symbols_list = data['symbols']

    # for symbol in symbols_list:
    #     print(symbol['rootSymbol'])

    #     for option in symbol['options']:
    #         print(option)

    json_response = response.json()
    print(response.status_code)
    print(json.dumps(json_response, indent=4))

else:
    print('Error with the request:', response.status_code, response.text)
