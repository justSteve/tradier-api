# Version 3.6.1    
import config, requests, json, sys


# #this file will be called by a CLI with the following arguments: 
# # symbol, expiration, center, width, quantity, type, duration, price

# # e.g. buildFly.py SPX 2023-08-29 4405 10 10 market day 1.0

# #using the CLI's arguments, parse the input to vars that maps to the string that becomes the 'data' params of the  payload for the Tradier API call
# #this set of parameters is an example of how to send data to Tradier's api. 
# response = requests.post('https://sandbox.tradier.com/v1/accounts/{}/orders'.format(config.ACCOUNT_ID_SAND)),
# data={'class': 'multileg', 'symbol': 'SPY', 'type': 'market', 'duration': 'day', 
#           'price': '1.0', 'option_symbol[0]': 'SPY190605C00282000', 'side[0]': 'buy_to_open', 
#           'quantity[0]': '10', 'option_symbol[1]': 'SPY190605C00286000', 'side[1]': 'buy_to_close', 
#           'quantity[1]': '10'},
# headers=headers
# print(response)
# print(type(response))

# json_response = response.json()
# print(response.status_code)
# print(json_response)

import requests

def construct_fly_parameters(center, width, exp_date):
    lower_strike = center - width
    upper_strike = center + width

    # Construct the option symbols based on the given information
    center_option_symbol = f"SPX{exp_date}C{center:08}"
    lower_option_symbol = f"SPX{exp_date}C{lower_strike:08}"
    upper_option_symbol = f"SPX{exp_date}C{upper_strike:08}"

    # Prepare the API call parameters
    api_data = {
        'class': 'multileg',
        'symbol': 'SPX',
        'type': 'market',
        'duration': 'day',
        'option_symbol[0]': lower_option_symbol,
        'side[0]': 'buy_to_open',
        'quantity[0]': '1',
        'option_symbol[1]': center_option_symbol,
        'side[1]': 'sell_to_open',
        'quantity[1]': '2',
        'option_symbol[2]': upper_option_symbol,
        'side[2]': 'buy_to_open',
        'quantity[2]': '1'
    }

    return api_data

# Define your parameters
center_strike = 4490
width = 10
exp_date = '230905'  # Assuming YYMMDD format for 1st August 2023

# Generate the API parameters
api_parameters = construct_fly_parameters(center_strike, width, exp_date)

# Make the API call to Tradier (replace YOUR_ACCESS_TOKEN and YOUR_ACCOUNT_ID)

headers = {
    'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_SAND_pjk), 
    'Accept': 'application/json'
}
response = requests.post('https://sandbox.tradier.com/v1/accounts/{}/orders'.format(config.ACCOUNT_ID_SAND_pjk),
                         headers=headers, data=api_parameters)


# Process the API response
try:
    if response.status_code == 201:
        print('Order placed successfully', response.json())
    else:
        print(f"Failed to place the order with status code {response.status_code}: {response.text}")
except requests.exceptions.JSONDecodeError:
    print(f"Could not decode JSON from response: {response.text}")
