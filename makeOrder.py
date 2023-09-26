import json

def transform_tos_to_tradier(tos_json):
    # Parse JSON into a Python dictionary
    tos_dict = json.loads(tos_json)
    
    # Extracting and Mapping fields
    if (tos_dict['Action']) == 'BUY': 
        type = 'debit' 
    else: type = 'credit'
    
    quantity = tos_dict['Contracts']
    symbol = tos_dict['Symbol']
    expiry = tos_dict['Expiry'].replace(' ', '')
    strikes = list(map(int, tos_dict['Strikes'].split('/')))
    
    # Formatting OCC symbol based on TOS information
    occ_symbols = [
        f"{symbol}{expiry}C{str(strike).zfill(5)}000" for strike in strikes
    ]   


    print(occ_symbols)
    # Construct Tradier query string
    
    query_string = f"class=multileg&symbol=" + symbol + "&duration=day&type=" + type + "&price=limit&stop=0&limit=0&range=0&session=normal&preview=false&legs="
    for i, strike in enumerate(strikes):
        side = "buy_to_open" if i % 2 == 0 else "sell_to_open"  # Adjust according to the actual order type
        print (i)
        query_string += f"&side[{i}]={side}&quantity[{i}]={quantity}&option_symbol[{i}]={occ_symbols[i]}"

    return query_string

# Example usage
tos_json = json.dumps({
    'Action': 'SELL',
    'Contracts': '-10',
    'Strat': 'Butterfly',
    'Symbol': 'SPX',
    'Shares': 100,
    'Expiry': '27 Jul 23',
    'Strikes': '4615/4625/4635',
    'Side': 'CALL',
    'Price': '@0.42 LMT'
})
tradier_query_string = transform_tos_to_tradier(tos_json)
print(tradier_query_string)
