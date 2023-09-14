import json

tradier_output = '{"positions":{"position":[{"cost_basis":284.00,"date_acquired":"2023-09-12T20:07:30.738Z","id":5184907,"quantity":1.00000000,"symbol":"SPXW230913P04425000"},{"cost_basis":-712.00,"date_acquired":"2023-09-12T20:07:30.738Z","id":5184908,"quantity":-2.00000000,"symbol":"SPXW230913P04430000"},{"cost_basis":443.00,"date_acquired":"2023-09-12T20:07:30.738Z","id":5184906,"quantity":1.00000000,"symbol":"SPXW230913P04435000"}]}}'

data = json.loads(tradier_output)

# Extract positions
positions = data['positions']['position']

# Initialize lists to collect option legs
bought_legs = []
sold_legs = []

# Variable to hold the number of contracts and total cost basis
num_contracts = 0
total_cost_basis = 0.0

# Process each position
for pos in positions:
    qty = int(pos['quantity'])
    cost_basis = float(pos['cost_basis'])
    symbol = pos['symbol']

    # Extract useful data from the symbol
    asset = symbol[:3]  # Assuming first three characters represent the asset
    #instead define the symbol to be all alpha characters up to the first digit
    exp_date = symbol[4:10]
    strike = float(symbol[-8:-3])  # Remove leading zeros
    option_type = 'CALL' if symbol[-3] == 'C' else 'PUT'

    # Calculate the total cost basis
    total_cost_basis += cost_basis

    # Separate bought and sold legs and use only unique strike prices
    if qty > 0:
        if strike not in bought_legs:
            bought_legs.append(strike)
        num_contracts = qty  # Update the number of contracts based on the long legs
    else:
        if strike not in sold_legs:
            sold_legs.append(strike)

# Sort the legs
bought_legs = sorted(bought_legs)
sold_legs = sorted(sold_legs)

# Calculate the limit price for the TOS order string
limit_price = total_cost_basis / num_contracts

# Create TOS string
tos_string = f"BUY +{num_contracts} BUTTERFLY {asset} {exp_date[2:4]} (Weeklys) {exp_date[4:]} SEP {exp_date[:2]} {bought_legs[0]}/{sold_legs[0]}/{bought_legs[-1]} {option_type} @ {limit_price:.2f} LMT"

print(tos_string)
