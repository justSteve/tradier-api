import config
import requests
import json
import sys
import pandas as pd
import re

def parse_cboe_identifier(identifier):
    """
    Parse a CBOE options identifier into its components.

    Parameters:
    - identifier (str): The CBOE options identifier string.

    Returns:
    - dict: A dictionary containing the components of the identifier.
    """
    
    # Find the first digit's index
    first_digit_index = re.search(r'\d', identifier).start()
    
    # Extract the underlying asset
    underlying_asset = identifier[:first_digit_index]

    # Extract the expiration date and reformat it
    expiration_date_str = identifier[first_digit_index:first_digit_index+6]
    expiration_date = f"20{expiration_date_str[:2]}-{expiration_date_str[2:4]}-{expiration_date_str[4:6]}"

    # Extract the option type
    option_type_char = identifier[first_digit_index+6]
    option_type = "Call" if option_type_char == "C" else "Put" if option_type_char == "P" else "Unknown"

    # Extract the strike price and reformat it
    strike_price_str = identifier[first_digit_index+7:]
    strike_price = float(strike_price_str) / 1000  # Assuming that the last three digits are decimal places

    # Create a dictionary to hold the components
    parsed_data = {
        "Underlying": underlying_asset,
        "Expiry": expiration_date,
        "Type": option_type,
        "Price": strike_price
    }

    return parsed_data




gexURL = "http://api.gexbot.com/spx/zero/gex?key=" + config.API_GEXBOT_KEY

gexURL = config.API_URL_GEXBOT + config.API_GEXBOT_KEY
# gexURL = ".format(config.API_GEXBOT_URL).format(config.API_GEXBOT_KEY)"
responseGex = requests.get(gexURL)


json_response = responseGex.json()
print(responseGex.status_code)
print(gexURL)
print(json_response)


url = "{}markets/options/lookup".format(config.API_BASE_URL)

headers = {
    'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk),
    'Accept': 'application/json'
}
response = requests.get(url,
                        params={'underlying': 'spx'},
                        headers=headers
                        )

# Check if the request was successful
if response.status_code == 200:

    # Extract the strikes
    data = response.json()

    symbols_list = data['symbols']

    for symbol in symbols_list:
        print(symbol['rootSymbol'])

        for option in symbol['options']:
            parsed_data = parse_cboe_identifier(option)
            

            strike_price = parsed_data['Price']
            expiry = parsed_data['Expiry']

            if 4400 <= strike_price <= 4450 and expiry == '2023-09-12':   

                    print(parsed_data)

                    responseQuote = requests.get('https://api.tradier.com/v1/markets/quotes',
                    params={'symbols': 'spx', 'greeks': 'true'},
                    #params={'symbols': {option}, 'greeks': 'true'},
                    headers={'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'}
                    )

                    json_response = responseQuote.json()
                    print(response.status_code)
                    print(json_response)

            # else:
            #         print()
            #         #print("Strike price is outside the range of 4400 to 4450.")

else:
    print('Error with the request:', response.status_code, response.text)


