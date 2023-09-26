#TradeLeg.py
from models.base_leg import BaseLeg

class TradierLeg(BaseLeg):
    @classmethod
    def from_dict(cls, data: dict) -> 'TradierLeg':
        return cls(
            broker="Tradier",
            id=data['id'],
            parent_id=data.get('parent_id', None),
            type_=data['type'],
            symbol=data['symbol'],
            side=data['side'],
            quantity=data['quantity'],
            status=data['status'],
            duration=data['duration'],
            price=data['price'],
            avg_fill_price=data['avg_fill_price'],
            exec_quantity=data['exec_quantity'],
            last_fill_price=data['last_fill_price'],
            last_fill_quantity=data['last_fill_quantity'],
            remaining_quantity=data['remaining_quantity'],
            create_date=data['create_date'],
            transaction_date=data['transaction_date'],
            class_name=data.get('class', None),
            option_symbol=data.get('option_symbol', None)
        )

    @staticmethod
    def validate_leg(data: dict) -> bool:
        required_fields = ['option_symbol', 'side']
        for field in required_fields:
            if field not in data:
                return False
        return True

#ends