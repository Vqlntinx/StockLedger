import json
from datetime import date
from abc import ABC, abstractmethod
from typing import List

from .domain import StockTrade, TradeType


class TradeRepository(ABC):
    @abstractmethod
    def add(self, trade: StockTrade) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[StockTrade]:
        pass


class FileTradeRepository(TradeRepository):
    def __init__(self, file_path="trades.json"):
        self.file_path = file_path
        self._trades = []
        self._load()

    def add(self, trade: StockTrade) -> None:
        self._trades.append(trade)
        self._save()

    def list_all(self) -> List[StockTrade]:
        return list(self._trades)

    def _load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._trades = [
                    StockTrade(
                        date=date.fromisoformat(t["date"]),
                        ticker=t["ticker"],
                        trade_type=TradeType(t["type"]),
                        price=t["price"],
                        quantity=t["quantity"],
                        fee=t["fee"],
                    )
                    for t in data
                ]
        except FileNotFoundError:
            self._trades = []

    def _save(self):
        raw = [
            {
                "date": t.date.isoformat(),
                "ticker": t.ticker,
                "type": t.trade_type.value,
                "price": t.price,
                "quantity": t.quantity,
                "fee": t.fee,
            }
            for t in self._trades
        ]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2, ensure_ascii=False)