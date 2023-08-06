
class Execution(object):
    def __init__(self, id: int = 0, quantity: float = 0, price: float = 0, taker_side: str = '', created_at: int = 0):
        self.id = id
        self.quantity = quantity
        self.price = price
        self.taker_side = taker_side
        self.created_at = created_at

    def __eq__(self, o):
        return self.id == o.id \
            and self.quantity == o.quantity \
            and self.price == o.price \
            and self.taker_side == o.taker_side \
            and self.created_at == o.created_at


class FiatAccount(object):
    def __init__(self, id: int = 0, currency: str = '', currency_symbol: str = '', balance: float = 0, reserved_balance: float = 0, pusher_channel: str = '', lowest_offer_interest_rate: float = 0, highest_offer_interest_rate: float = 0, exchange_rate: float = 0, currency_type: str = ''):
        self.id = id
        self.currency = currency
        self.currency_symbol = currency_symbol
        self.balance = balance
        self.reserved_balance = reserved_balance
        self.pusher_channel = pusher_channel
        self.lowest_offer_interest_rate = lowest_offer_interest_rate
        self.highest_offer_interest_rate = highest_offer_interest_rate
        self.exchange_rate = exchange_rate
        self.currency_type = currency_type

    def __eq__(self, o):
        return self.id == o.id \
            and self.currency == o.currency \
            and self.currency_symbol == o.currency_symbol \
            and self.balance == o.balance \
            and self.reserved_balance == o.reserved_balance \
            and self.pusher_channel == o.pusher_channel \
            and self.lowest_offer_interest_rate == o.lowest_offer_interest_rate \
            and self.highest_offer_interest_rate == o.highest_offer_interest_rate \
            and self.exchange_rate == o.exchange_rate \
            and self.currency_type == o.currency_type


class Page(object):
    def __init__(self, currentPage: int = 0, totalPages: int = 0, models: list = []):
        self.current_page = currentPage
        self.total_pages = totalPages
        self.models = models

    def __eq__(self, o):
        res1 = self.current_page == o.current_page \
            and self.total_pages == o.total_pages
        if (res1 and self.models == o.models) == True:
            return True
        if (res1 and len(self.models) == len(o.models)) == False:
            return False
        if not res1:
            return False
        for i in range(0, len(self.models)):
            if self.models[i] != o.models[i]:
                return False
        return True
