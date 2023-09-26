# base_leg.py
class BaseLeg:
    def __init__(
            self, 
            broker: str, 
            id: str, 
            parent_id: str, 
            type_: str, 
            symbol: str, 
            side: str, 
            quantity: int, 
            status: str, 
            duration: str, 
            price: float, 
            avg_fill_price: float, 
            exec_quantity: int, 
            last_fill_price: float, 
            last_fill_quantity: int, 
            remaining_quantity: int, 
            create_date: str, 
            transaction_date: str, 
            class_name: str, 
            option_symbol: str = None
        ):
        self.broker = broker
        self.id = id
        self.parent_id = parent_id
        self.type = type_
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.status = status
        self.duration = duration
        self.price = price
        self.avg_fill_price = avg_fill_price
        self.exec_quantity = exec_quantity
        self.last_fill_price = last_fill_price
        self.last_fill_quantity = last_fill_quantity
        self.remaining_quantity = remaining_quantity
        self.create_date = create_date
        self.transaction_date = transaction_date
        self.class_name = class_name
        self.option_symbol = option_symbol

#ends