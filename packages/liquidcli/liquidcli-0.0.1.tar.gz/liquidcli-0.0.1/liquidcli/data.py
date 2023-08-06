
class Execution(object):
    def __init__(self, id: int = 0, quantity: float = 0, price: float = 0, takerSide: str = '', createdAt: int = 0):
        self.id = id
        self.quantity = quantity
        self.price = price
        self.takerSide = takerSide
        self.createdAt = createdAt
        pass


class FiatAccount(object):
    def __init__(self, id: int = 0):
        self.id = id


class Page(object):
    def __init__(self, currentPage: int = 0, totalPages: int = 0, models: list = []):
        self.currentPage = currentPage
        self.totalPages = totalPages
        self.models = models
        pass
