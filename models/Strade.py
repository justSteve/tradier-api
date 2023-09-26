# In Strade.py

from typing import List
from models.TradierOrder import TradierOrder
from utils import decode_occ_symbol, encode_occ_symbol

class Strade:
    def __init__(self, strade_id: str, strike: float, type_: str, num_legs: int):
        self.id = strade_id
        self.strike = strike
        self.type = type_  # 'call' or 'put'
        self.num_legs = num_legs  # Added num_legs attribute
        self.orders = []  # List of TradierOrder instances

    def add_order(self, order: TradierOrder) -> None:
        if not isinstance(order, TradierOrder):
            raise ValueError("The provided order is not an instance of TradierOrder.")
        
        # Add debugging lines here to inspect variables
        print("=== Debugging Start ===")
        print(f"Strade Type: {self.type}")
        print(f"Strade Strike: {self.strike}")
        
        for leg in order.legs:
            decoded_symbol = decode_occ_symbol(leg.option_symbol)
            print(f"Leg Option Symbol: {leg.option_symbol}")
            print(f"Decoded Symbol Type: {decoded_symbol['type']}")
            print(f"Decoded Symbol Strike: {decoded_symbol['strike']}")
        
        print("=== Debugging End ===")
        
    @staticmethod
    def validate_strade(data: dict) -> bool:
        required_fields = ['strade_id', 'strike', 'type']
        for field in required_fields:
            if field not in data:
                return False
        return True
