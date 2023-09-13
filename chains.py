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


# url = "{}markets/options/chains".format(config.API_BASE_URL)
url = "{}markets/options/lookup".format(config.API_BASE_URL)

headers = {
    'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN),
    'Accept': 'application/json'
}
response = requests.get(url,
                        # params={'symbol': 'spx', 'expiration': '2023-09-06', 'greeks': 'true'},
                        params={'underlying': 'spx'},
                        # params={'symbol': sys.argv[1], 'expiration': sys.argv[2], 'greeks': 'true'},
                        headers=headers
                        )

# Check if the request was successful
if response.status_code == 200:

    # Extract the strikes
    strikes = response.json()['options']['option']

    # Flatten the JSON
    # for strike in strikes:
    #     greeks = strike.pop('greeks')
    #     for key, value in greeks.items():
    #         strike[f'greeks_{key}'] = value

    # # Convert to a DataFrame
    # df = pd.DataFrame(strikes)

    # # Write to Excel
    # df.to_excel('strikes1.xlsx', index=False)

    # Filter out strikes with mid_iv of 0
    filtered_strikes = [strike for strike in strikes if strike.get('greeks')
                        and strike['greeks']['mid_iv'] != 0
                        # and strike['option_type'] == 'put'
                        ]

    # Find the index of the strike with the minimum mid_iv
    LIV = 0
    min_index = 0
    min_mid_iv = float('inf')
    for index, strike in enumerate(filtered_strikes):
        if strike['greeks']['mid_iv'] < min_mid_iv:
            min_mid_iv = strike['greeks']['mid_iv']
            min_index = index
            LIV = strike['strike']

    print(LIV, strike['greeks']['mid_iv'])
    print()

    # Get the 5 strikes both above and below the minimum from the original order
    lower_strikes = filtered_strikes[max(min_index - 10, 0):min_index]
    higher_strikes = filtered_strikes[min_index + 1:min_index + 11]

    # print(lower_strikes)
    # print(higher_strikes)

    # print(' strikes with the next lower IV values:')
    # for strike in reversed(lower_strikes): # Reversing to show in descending order
    #     print(strike['strike'], strike['option_type'], strike['greeks']['mid_iv'])

    # print(' strikes with the next higher IV values:')
    # for strike in higher_strikes:
    #     print(strike['strike'], strike['option_type'], strike['greeks']['mid_iv'])
else:
    print('Error with the request:', response.status_code, response.text)

# json_response = response.json()
# print(response.status_code)
# print(json_response)
