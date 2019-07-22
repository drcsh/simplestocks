from tabulate import tabulate
from exchange import ExchangeBuilder, InvalidStockException
from trade import InvalidTradeException

"""
    CLI for using this program
"""


def main():
    cli = CLI()
    cli.run()


class UserInterrupt(Exception):
    pass


class CLI(object):
    """
        A quick and dirty CLI to sit in front of the Exchange and make it easier to work with.
    """

    def __init__(self):
        print("Loading SimpleStocks...")

        self.exchange = ExchangeBuilder.build()

    def run(self):
        """
        Central loop. Runs until program is exited by the user.

        :return:
        """
        print(f"Welcome to SimpleStocks. You are trading on the {self.exchange}.")
        while True:
            input = self._prompt_user("Enter Action: (a)ll share index, (l)ist, (b)uy, (s)ell, (q)uit")
            try:
                self.interpret_user_action_request(input)
            except UserInterrupt:
                print("Action Cancelled")

            print("")  # Add an extra newline before asking for their next action

    def interpret_user_action_request(self, input):
        """
        Interpret the user's request to do something and present that functionality.
        :param input:
        :return:
        """
        input = input.lower()
        # quit
        if input in ["exit", "q", "quit"]:
            print("Thank you for using SimpleStocks!")
            exit(0)

        if input in ["all share index", "all", "index", "a"]:
            self._show_share_index()
            return

        if input in ["list", "l"]:
            self._show_stock_list()
            return

        if input in ["buy", "b"]:
            self._buy_stock()
            return

        if input in ["sell", "s"]:
            self._sell_stock()
            return

        # If we got this far...
        print(f"Sorry, I don't know how to {input}")

    def _show_share_index(self):
        """
        Shows the All Share Index
        :return:
        """
        raw_index = self.exchange.calculate_all_share_index()
        print(f" {self.exchange.name} All Share Index: {round(raw_index, 3)}")

    def _show_stock_list(self):
        """
        List stocks in the terminal
        :return:
        """

        print(" Stock List:")

        headers = ["Symbol", "Type", "Last Dividend", "Fixed Dividend", "Dividend Yield", "P/E Ratio", "Price"]

        table = []
        for stock in self.exchange.stocks.values():
            row = [stock.symbol,
                   stock.type,
                   stock.last_dividend,
                   stock.fixed_dividend or '',
                   round(stock.calculate_dividend_yield(), 3),
                   round(stock.calculate_price_to_earnings_ratio(), 3),
                   stock.calculate_price()]
            table.append(row)

        print(tabulate(table, headers=headers, tablefmt="github"))
        return

    def _buy_stock(self):
        """
        Prompts the user for information needed to buy a stock, confirms they want to do this and then carries out the
        transaction
        """
        stock_symbol, quantity, price = self._get_transaction_details_from_user("buy")

        confirm = self._get_user_confirm(f"You want to buy {quantity} of {stock_symbol} at {price}p?")
        if not confirm:
            raise UserInterrupt("Cancelled")

        # if we got this far, try to purchase. They may still fail here if, for example, the price was negative
        try:
            self.exchange.buy_stock(stock_symbol, quantity, price)
            print("Purchase Successful")

        except (InvalidStockException, InvalidTradeException) as e:
            print(str(e))

    def _sell_stock(self):
        """
        Counterpart to _buy_stock
        """
        stock_symbol, quantity, price = self._get_transaction_details_from_user("sell")

        confirm = self._get_user_confirm(f"You want to sell {quantity} of {stock_symbol} at {price}p?")
        if not confirm:
            raise UserInterrupt("Cancelled")

        # if we got this far, try to purchase. They may still fail here if, for example, the price was negative
        try:
            self.exchange.buy_stock(stock_symbol, quantity, price)
            print("Sale Successful")

        except (InvalidStockException, InvalidTradeException) as e:
            print(str(e))

    def _get_transaction_details_from_user(self, transaction_name):
        """
        Fetches input from the user required to either buy or sell stock. Returns the stock_symbol, quantity and price
        in that order

        :param str transaction_name: "buy" or "sell" so that the user can by prompted appropriately.
        :return: stock_symbol, quantity, price
        :rtype tuple: (str, int, int)
        """

        # Keep prompting them until they choose a valid stock or quit
        valid_stock = False
        while not valid_stock:
            stock_symbol = self._prompt_user(
                f"Please enter the stock symbol (e.g. ABC) of the one you wish to {transaction_name}, or c to cancel."
            )

            self._check_input_for_user_cancel(stock_symbol)

            # upper it, so it matches the stock symbol
            stock_symbol = stock_symbol.upper()

            # check that it's valid
            try:
                self.exchange.get_stock(stock_symbol)
                valid_stock = True
            except InvalidStockException as e:
                print(str(e))

        # ask for a quantity and price. These must convert to int
        valid_quantity = False

        while not valid_quantity:
            try:
                quantity = self._prompt_user(
                    f"How many stocks would you like to {transaction_name}? (or c to cancel)"
                )
                self._check_input_for_user_cancel(quantity)

                quantity = int(quantity)
                valid_quantity = True

            except ValueError:
                print("Sorry, the quantity was invalid. Please enter a whole number > 0.")

        valid_price = False

        while not valid_price:
            try:
                price = self._prompt_user(
                    f"How much (in pennies) would you like to {transaction_name} them for? (or c to cancel)"
                )
                self._check_input_for_user_cancel(price)

                price = int(price)
                valid_price = True

            except ValueError:
                print("Sorry, the price was invalid. Please enter a whole number of pennies > 0. For example, if you "
                      f"want to {transaction_name} at £1.50 per stock, please type 150.")

        return stock_symbol, quantity, price

    def _check_input_for_user_cancel(self, input):
        """
        Checks the input to see if the user if trying to cancel. Raises a UserInterrupt exception if the input looks
        like an attempt to cancel (i.e. "c", "q", "quit")

        :param input:
        :raises UserInterupt:
        """
        if input.lower() in ['c', 'cancel', 'q', 'quit', 'no']:
            raise UserInterrupt("Cancelled")

    def _get_user_confirm(self, msg):
        """
        Ask the user to confirm an action, more restrictive than the counterpart for checking user cancellation. This
        will only except explicit yes responses. Allows the calling function to determine what to do with this.

        :param str msg: what to prompt them with. (y/n) and a prompt will be added at the end.
        :return: True if they confirmed, False otherwise.
        :rtype bool:
        """

        confirm = self._prompt_user(f"{msg} (y/n)")

        return confirm.lower() in ['y', 'yes']

    def _prompt_user(self, msg):
        """
        Utility function for prompting the user for input. Adds a newline before and after the message,
        as well as prompt character.

        :param str msg: message to display on prompt
        :return: Output. Stripped.
        :rtype str:
        """
        raw_input = input(f"\n{msg}\n> ")
        return raw_input.strip()


if __name__ == '__main__':
    main()
