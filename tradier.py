import config, requests, json, sys


url = "{}markets/quotes".format(config.API_BASE_URL)

headers = {
    'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN), 
    'Accept': 'application/json'
}

if len(sys.argv) > 1:
    print(f"Hello, {sys.argv[1]}!")
else:
    print("No arguments were passed.")
    exit()

response = requests.get(url,
    params={'symbols': sys.argv[1]},
    headers=headers
)



str = json.dumps(response.json(), indent=4)
print(str)

# options_url = '{}markets/options/chains'.format(config.API_BASE_URL)

# response = requests.get(options_url,
#     params={'symbol': 'TSLA', 'expiration': '2023-06-14'},
#     headers=headers
# )

# print(response.json())

# tesla_call_symbol = 'TSLA200522C00850000'

# order_url = '{}accounts/{}/orders'.format(config.API_BASE_URL, config.ACCOUNT_ID)

# response = requests.post(order_url,
#     data={'class': 'option', 'symbol': 'TSLA', 'option_symbol': tesla_call_symbol, 'side': 'buy_to_open', 'quantity': '3', 'type': 'market', 'duration': 'day'},
#     headers=headers
# )

# print(response.json())

# orders = requests.get(order_url, headers=headers)

# print(orders.json())