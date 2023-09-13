import config
import requests
import json
import sys
import pandas as pd
import re

def parse_iso_identifier(expiry, strike):
    """
    Generate a iso options identifier 

    Returns:
    - dict: A dictionary containing the components of the identifier.
    """
    
    # Retrieve the identifier from combined_data
    # identifier = combined_data.get("Quotes", {}).get(iso_key, {}).get("identifier_field_here", "")
    # if not identifier:
    #     return {"error": "Identifier not found"}

    # # Find the first digit's index
    # first_digit_index = re.search(r'\d', identifier).start()
    
    # # Extract the underlying asset
    # underlying_asset = identifier[:first_digit_index]

    # # Extract the expiration date and reformat it
    # expiration_date_str = identifier[first_digit_index:first_digit_index+6]
    # expiration_date = f"20{expiration_date_str[:2]}-{expiration_date_str[2:4]}-{expiration_date_str[4:6]}"


    # combined_data = {"GEXBOT_Data": {"strikes": relevant_strikes}, "Quotes": {}}

import os
import json
from datetime import datetime

def save_json_to_date_folder(json_data):
    # Convert the timestamp to a datetime object
    timestamp = json_data.get("timestamp", None)
    if timestamp is None:
        print("Timestamp not found in JSON.")
        return

    # Convert timestamp to seconds from milliseconds
    timestamp /= 1000.0

    # Format datetime to YYYY_MM_DD
    dt_object = datetime.fromtimestamp(timestamp)
    folder_name = dt_object.strftime('%Y_%m_%d')

    # Check if folder exists, if not create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Find the next available file name
    file_count = 1
    while True:
        file_name = f"{file_count:05d}.json"
        file_path = os.path.join(folder_name, file_name)
        if not os.path.exists(file_path):
            break
        file_count += 1

    # Write the json data to the file
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)

# Sample API JSON response
api_response = {
    'timestamp': 1694030398224,
    'ticker': 'SPX',
    # ... other fields
}



gexURL = config.API_URL_GEXBOT + config.API_GEXBOT_KEY
# gexURL = ".format(config.API_GEXBOT_URL).format(config.API_GEXBOT_KEY)"
responseGex = requests.get(gexURL)


gex_data = responseGex.json()
print(responseGex.status_code)
print(gex_data)
# Call the function to save the JSON data
save_json_to_date_folder(gex_data)

relevant_strikes = []
for strike_info in gex_data.get("strikes", []):
    strike = strike_info.get("strike")
    if 4400 <= strike <= 4450:
        relevant_strikes.append(strike)

for strike in relevant_strikes:
    # Construct the iso ID here based on the strike, expiry, and type (put or call)
    iso_id = f"SPX{strike}"  # use the same pattern as TOS to generate the iso ID
    
    responseQuote = requests.get('https://api.tradier.com/v1/markets/quotes',
                                 params={'symbols': iso_id, 'greeks': 'true'},
                                 headers={'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk),
                                          'Accept': 'application/json'})
    
    quote_data = responseQuote.json()
    combined_data = {"GEXBOT_Data": {"strikes": relevant_strikes}, "Quotes": {}}

    # Save the quote data for the iso ID
    combined_data["Quotes"][iso_id] = quote_data


    json_response = responseQuote.json()
    print(responseQuote.status_code)
    print(json_response)


# url = "{}markets/options/lookup".format(config.API_BASE_URL)

# headers = {
#     'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk),
#     'Accept': 'application/json'
# }
# response = requests.get(url,
#                         params={'underlying': 'spx'},
#                         headers=headers
#                         )

# # Check if the request was successful
# if response.status_code == 200:

#     # Extract the strikes
#     data = response.json()

#     symbols_list = data['symbols']

#     for symbol in symbols_list:
#         print(symbol['rootSymbol'])

#         for option in symbol['options']:
#             parsed_data = parse_iso_identifier(option)
            

#             strike_price = parsed_data['Price']
#             expiry = parsed_data['Expiry']

#             if 4400 <= strike_price <= 4450 and expiry == '2023-09-07':   

#                     print(parsed_data)

#                     responseQuote = requests.get('https://api.tradier.com/v1/markets/quotes',
#                     params={'symbols': 'spx', 'greeks': 'true'},
#                     #params={'symbols': {option}, 'greeks': 'true'},
#                     headers={'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'}
#                     )

#                     json_response = responseQuote.json()
#                     print(response.status_code)
#                     print(json_response)

#             # else:
#             #         print()
#             #         #print("Strike price is outside the range of 4400 to 4450.")

# else:
#     print('Error with the request:', response.status_code, response.text)


