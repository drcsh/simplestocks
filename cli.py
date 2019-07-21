from tabulate import tabulate
from exchange import Exchange, ExchangeBuilder
"""
    CLI for using this program
"""


def main():

    print("Loading SimpleStocks...")

    cli = CLI()

    print("Weclome to SimpleStocks, trading on the f{exchange.name}")



class CLI(object):

    def __init__(self):
        self.exchange = ExchangeBuilder.build()

    def run(self):
        while True:
            input = self.get_user_action()
            self.interpret_action(input, self.exchange)

    def interpret_action(input, exchange):

        # quit
        if input in ["exit", "q", "quit"]:
            print("Thank you for using SimpleStocks")
            exit(0)

        # list stocks
        if input in ["list", "l"]:
            print("Stock List:")

            headers = ["Symbol", "Type", "Last Dividend", "Fixed Dividend", "Price"]

            table = []
            for stock in exchange.stocks.values():
                row = [stock.symbol, stock.type, stock.last_dividend, stock.fixed_dividend,  stock.calculate_price()]
                table.append(row)

            print(tabulate(table, headers))

    def get_user_action():
        raw_input = input("Enter Action: list (l), buy (b), sell (s), exit (q) \n>>> ")
        return raw_input.strip()


if __name__ == '__main__':
    main()