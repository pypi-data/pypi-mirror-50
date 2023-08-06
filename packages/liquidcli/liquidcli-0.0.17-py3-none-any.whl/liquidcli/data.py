from dataclasses import dataclass
from typing import List


@dataclass
class Execution:
    id: int = ''
    quantity: float = 0
    price: float = 0
    taker_side: str = ''
    created_at: int = 0


@dataclass
class FiatAccount:
    id: int = 0
    currency: str = ''
    currency_symbol: str = ''
    balance: float = 0
    reserved_balance: float = 0
    pusher_channel: str = ''
    lowest_offer_interest_rate: float = 0
    highest_offer_interest_rate: float = 0
    exchange_rate: float = 0
    currency_type: str = ''


@dataclass
class Page:
    current_page: int
    total_pages: int
    models: List[Execution]
