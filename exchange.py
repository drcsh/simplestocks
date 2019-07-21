from stock import Stock, CommonStock, PreferredStock
from trade import Trade

from functools import reduce


class Exchange(object):

    def __init__(self, stocks):
        self.stocks = stocks

    def calculate_all_share_index(self):
        """
        Calculates the all share index value in pennies.

        This is defined as the geometric mean of all stocks listed on the exchange (i.e. the nth root of the product
        of all stock prices, where n = the total number of stocks)

        :return:
        :rtype: float - not rounded.
        """

        if len(self.stocks) < 1:
            return 0

        # Get a list of all stock prices
        stock_prices = [x.calculate_price() for x in self.stocks]

        # calculate the product of that list
        stock_price_product = reduce(lambda x, y: x * y, stock_prices)

        # Return the nth root of the product where n = len(self.stocks)
        return stock_price_product ** (1 / len(self.stocks))