#TradierOrder.py

from typing import List, Union
from models.base_order import BaseOrder
from models.TradierLeg import TradierLeg

class TradierOrder(BaseOrder):
    @classmethod
    
    def from_dict(cls, data: dict) -> 'TradierOrder':
        legs_data = data.get('leg', [])
        legs = [TradierLeg.from_dict(leg_data) for leg_data in legs_data]
        
        return cls(
            strade_id=None,  # Added strade_id with default value None
            broker="Tradier",
            order_id=data['id'],
            num_legs=len(legs),  # Calculated from the length of the legs list
            strategy=data.get('strategy', None),
            legs=legs,
            class_name=data.get('class', None)
        )
    def add_leg(self, leg):
        self.legs.append(leg)
        
        
    @staticmethod
    def validate_order(data: dict) -> bool:
        required_fields = ['id', 'strategy']
        for field in required_fields:
            if field not in data:
                raise ValueError("Invalid. Missing required field: {field}")
    

        # Specific validation for 'butterfly' strategy
        if data['strategy'].lower() == 'butterfly':

            legs_data = data.get('leg', [])
            if len(legs_data) != 3:
                myLen = len(legs_data)
                raise ValueError("Butterflies required 3 legs. We found {myLen}")
            
            shorts = [leg for leg in legs_data if leg.get('side') == 'sell_to_open']
            longs = [leg for leg in legs_data if leg.get('side') == 'buy_to_open']
            
            if len(shorts) != 1 or len(longs) != 2:
                raise ValueError("Mismatch of longs to shorts")
            
            short_quantity = shorts[0].get('quantity', 0)
            long_quantity_sum = sum(leg.get('quantity', 0) for leg in longs)
            
            if short_quantity != long_quantity_sum:
                raise ValueError("Invalid quantity tween longs and shorts")

        return True

#ends
