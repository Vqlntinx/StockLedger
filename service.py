from collections import defaultdict
from typing import Dict, Tuple, List
from datetime import date

from .domain import StockTrade, TradeType
from .repository import TradeRepository


class RealizedPLCalculator:
    """Strategy Pattern: 다른 방식의 손익 계산기를 교체할 수 있음"""
    def calculate(self, trades: List[StockTrade], ticker: str) -> float:
        realized = 0.0
        avg_buy_price = None
        total_qty = 0

        # 평균단가 방식
        for t in trades:
            if t.ticker != ticker:
                continue

            if t.trade_type == TradeType.BUY:
                total_cost_before = (avg_buy_price or 0) * total_qty
                total_cost_after = total_cost_before + (t.price * t.quantity + t.fee)
                total_qty += t.quantity
                avg_buy_price = total_cost_after / total_qty

            elif t.trade_type == TradeType.SELL:
                realized += (t.price - avg_buy_price) * t.quantity - t.fee
                total_qty -= t.quantity

        return realized


class StockService:
    def __init__(self, repo: TradeRepository, pl_calculator: RealizedPLCalculator):
        self.repo = repo
        self.pl_calculator = pl_calculator

    def add_trade(self, trade: StockTrade):
        self.repo.add(trade)

    def get_positions(self) -> Dict[str, Dict[str, float]]:
        """종목별 보유 현황"""
        trades = self.repo.list_all()
        position = defaultdict(lambda: {"qty": 0, "total_cost": 0.0})

        for t in trades:
            if t.trade_type == TradeType.BUY:
                position[t.ticker]["qty"] += t.quantity
                position[t.ticker]["total_cost"] += t.price * t.quantity + t.fee

            elif t.trade_type == TradeType.SELL:
                position[t.ticker]["qty"] -= t.quantity
                position[t.ticker]["total_cost"] -= 0  # 평균단가 유지 → total_cost는 유지 가능

        for ticker in position.keys():
            pos = position[ticker]
            pos["avg_price"] = pos["total_cost"] / pos["qty"] if pos["qty"] > 0 else 0.0

        return position

    def get_realized_pl(self) -> float:
        """모든 종목 총 실현손익"""
        trades = self.repo.list_all()
        tickers = {t.ticker for t in trades}
        total = 0.0
        for tic in tickers:
            total += self.pl_calculator.calculate(trades, tic)
        return total

    def get_realized_pl_by_ticker(self, ticker: str) -> float:
        trades = self.repo.list_all()
        return self.pl_calculator.calculate(trades, ticker)
