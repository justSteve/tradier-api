#base_order.py
from typing import List
from models.base_leg import BaseLeg

class BaseOrder:
    def __init__(
            self, 
            strade_id: str, 
            broker: str, 
            order_id: str, 
            num_legs: int, 
            strategy: str, 
            legs: List[BaseLeg],
            class_name: str
        ):
        if not 1 <= len(legs) <= 4:
            raise ValueError("An order must have between 1 to 4 legs.")
        if len(legs) != num_legs:
            raise ValueError("Mismatch between provided number of legs and actual legs.")
        
        self.strade_id = strade_id
        self.broker = broker
        self.order_id = order_id
        self.num_legs = num_legs
        self.strategy = strategy
        self.legs = legs  
        self.class_name = class_name
#ends