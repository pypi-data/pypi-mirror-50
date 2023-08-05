from dateutil.parser import parse


class Payment:
    def __init__(self, id: str, address: str, amount: float, created_at: str, data: dict, symbol: str):
        self.id = id
        self.address = address
        self.amount = amount
        self.created_at = parse(created_at)
        self.data = data
        self.symbol = symbol
