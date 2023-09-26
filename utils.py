import re

def decode_occ_symbol(symbol: str):
    """
    Decode an OCC option symbol into its components.
    
    :param symbol: The OCC option symbol.
    :return: Dictionary with components of the option symbol.
    """
    # Find all alphabetical substrings
    alpha_parts = re.findall(r'[A-Za-z]+', symbol)
    
    # Find all numerical substrings
    numeric_parts = re.findall(r'\d+', symbol)
    
    if len(alpha_parts) < 1 or len(numeric_parts) < 2:
        raise ValueError("Invalid OCC symbol format.")
    
    underlying = alpha_parts[0]
    expiry = numeric_parts[0]
    option_type = alpha_parts[1]
    strike = float(numeric_parts[1]) / 100
    
    return {
        'underlying': underlying,
        'expiry': expiry,
        'type': option_type,
        'strike': strike
    }

def encode_occ_symbol(underlying: str, expiry: str, option_type: str, strike: float) -> str:
    """
    Encode components into an OCC option symbol.
    
    :param underlying: The underlying security identifier.
    :param expiry: Expiration date in the format yymmdd.
    :param option_type: 'C' for call, 'P' for put.
    :param strike: The strike price.
    :return: The OCC option symbol.
    """
    # Convert the strike price to the correct format
    strike_str = str(int(strike * 100)).zfill(8)
    
    return f"{underlying}{expiry}{option_type}{strike_str}"

# Test the functions
symbol = "SPXW230922C04305000"
decoded = decode_occ_symbol(symbol)
print(decoded)

encoded = encode_occ_symbol(decoded['underlying'], decoded['expiry'], decoded['type'], decoded['strike'])
print(encoded)
