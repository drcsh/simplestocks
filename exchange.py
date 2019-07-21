import time

from stock import Stock, CommonStock, PreferredStock
from trade import Trade

from functools import reduce


class InvalidStockException(Exception):
    """
        Exception for Exchange to throw when it has been given a bad stock identifier to work with.
    """
    pass


class ExchangeBuilder(object):

    def _load_stocks(self):
        """
        Stub. Should connect to a DB or something sensible

        :return: List of stocks to be loaded into the exchange
        :rtype dict: stock_symbol : Stock
        """

        stocks = {
            "TEA": CommonStock("TEA", 100, 0),
            "POP": CommonStock("POP", 100, 8),
            "ALE": CommonStock("ALE", 60, 23),
            "GIN": PreferredStock("GIN", 100, 8, 2),
            "JOE": CommonStock("JOE", 100, 8),
        }

        return stocks

    def build(self):
        """
        Creates an Exchange with some default stocks in it.

        In real life would do a lot more.
        :return:
        :rtype Exchange:
        """

        stocks = self._load_stocks()
        return Exchange(stocks)


class Exchange(object):
    """
        Represents an exchange. Holds a number of stocks which can be traded.
    """

    def __init__(self, stocks):

        assert isinstance(stocks, dict)

        self.stocks = stocks

    def get_stock(self, stock_symbol):
        """
        Fetches the Stock object with that stock_symbol. Throws an exception if it's not traded on this exchange.

        :param stock_symbol:
        :return:
        :rtype Stock:
        :raises InvalidStockException: the given stock symbol isn't found.
        """
        picked_stock = self.stocks.get(stock_symbol)

        if not picked_stock:
            raise InvalidStockException(f"Stock '{stock_symbol}' is not traded on this exchange!")

        return picked_stock

    def get_stock_price(self, stock_symbol):
        """
        Quotes the price of the requested Stock.

        :param str stock_symbol: the stock you want to know about
        :return: its price in pennies
        :rtype: int
        :raises InvalidStockException: if the stock symbol given is invalid.
        """
        picked_stock = self.get_stock(stock_symbol)
        return picked_stock.calculate_price()

    def buy_stock(self, stock_symbol, quantity, price):
        """
        Look up a stock by stock_symbol and record a Buy trade against it.

        This is just a friendly wrapper for record_trade on a Stock, but it's here for a couple of reasons, 1: to
        abstract away the interior workings of the exchange, 2: to provide a place to build more features, like adding
        a transaction fee, etc.

        :param str stock_symbol: identifier for the stock
        :param int quantity: number of stock to buy
        :param int price: price in pennies
        :raises InvalidStockException: wrong stock_symbol
        :raises InvalidTradeException: quantity or price are invalid
        """
        picked_stock = self.get_stock(stock_symbol)

        timestamp = time.time()
        new_trade = Trade(
            timestamp,
            quantity,
            Trade.BUY_INDICATOR,
            price
        )

        picked_stock.record_trade(new_trade)

    def sell_stock(self, stock_symbol, quantity, price):
        """
        Look up a stock by stock_symbol and record a Sell trade against it.

        :param str stock_symbol: identifier for the stock
        :param int quantity: number of stock to sell
        :param int price: price in pennies
        :raises InvalidStockException: wrong stock_symbol
        :raises InvalidTradeException: quantity or price are invalid
        """
        picked_stock = self.get_stock(stock_symbol)

        timestamp = time.time()
        new_trade = Trade(
            timestamp,
            quantity,
            Trade.SELL_INDICATOR,
            price
        )

        picked_stock.record_trade(new_trade)

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
        stock_prices = [x.calculate_price() for x in self.stocks.values()]

        # calculate the product of that list
        stock_price_product = reduce(lambda x, y: x * y, stock_prices)

        # Return the nth root of the product where n = len(self.stocks)
        return stock_price_product ** (1 / len(self.stocks))