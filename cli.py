from datetime import datetime
from .domain import StockTrade, TradeType
from .service import StockService, RealizedPLCalculator
from .repository import FileTradeRepository


class CLI:
    def __init__(self):
        repo = FileTradeRepository()
        calculator = RealizedPLCalculator()
        self.service = StockService(repo, calculator)

    def run(self):
        while True:
            print("\n=== StockLedger Mini ===")
            print("1. Add trade")
            print("2. View positions")
            print("3. View realized P/L")
            print("4. View realized P/L by ticker")
            print("0. Exit")
            choice = input("Select: ")

            if choice == "1":
                self.add_trade()
            elif choice == "2":
                self.view_positions()
            elif choice == "3":
                self.view_total_pl()
            elif choice == "4":
                self.view_ticker_pl()
            elif choice == "0":
                print("Bye!")
                break

    def add_trade(self):
        date_str = input("Date (YYYY-MM-DD): ")
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()

        ticker = input("Ticker: ").upper()

        ttype = input("Type (BUY/SELL): ").upper()
        trade_type = TradeType.BUY if ttype == "BUY" else TradeType.SELL

        price = float(input("Price: "))
        qty = int(input("Quantity: "))
        fee = float(input("Fee (0 for none): "))

        trade = StockTrade(dt, ticker, trade_type, price, qty, fee)
        self.service.add_trade(trade)

        print("✔ Trade added.")

    def view_positions(self):
        pos = self.service.get_positions()
        for ticker, info in pos.items():
            print(f"\n[{ticker}]")
            print(f"Quantity: {info['qty']}")
            print(f"Average Price: {info['avg_price']:.2f}")
            print(f"Total Cost: {info['total_cost']:.2f}")

    def view_total_pl(self):
        total = self.service.get_realized_pl()
        print(f"Total Realized P/L: {total:.2f}")

    def view_ticker_pl(self):
        ticker = input("Ticker: ").upper()
        pl = self.service.get_realized_pl_by_ticker(ticker)
        print(f"{ticker} Realized P/L: {pl:.2f}")
