from dataclasses import dataclass
from datetime import date
from enum import Enum


class TradeType(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class StockTrade:
    date: date
    ticker: str
    trade_type: TradeType
    price: float
    quantity: int
    fee: float = 0.0