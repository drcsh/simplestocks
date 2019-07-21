import time
from abc import ABC, abstractclassmethod

from trade import Trade


class Stock(ABC):
    """
    Abstract Base Class class for all Stock objects. Holds common functions.
    """

    TYPE_PREFERRED = "Preferred"
    TYPE_COMMON = "Common"

    def __init__(self, symbol, par_value, last_dividend):

        assert len(symbol) < 4
        assert isinstance(par_value, int)
        assert isinstance(last_dividend, int)

        self.symbol = symbol.upper()
        self.par_value = par_value
        self.last_dividend = last_dividend
        self.fixed_dividend = None
        self.trades = []

    @abstractclassmethod
    def calculate_dividend_yield(self):
        """
        Calculated differently depending on stock type. Implemented by child classes.
        :return:
        """
        pass

    def record_trade(self, trade):
        """
        Record a trade on this Stock.

        :param trade:
        :return:
        :raises TypeError: did not receive a Trade object.
        """
        if not isinstance(trade, Trade):
            raise TypeError("Can only record Trade objects!")

        self.trades.append(trade)

    def calculate_price(self):
        """
        Calculate the stock price in pence from the sum of the price * quantity, divided by the quantity of all trades
        in the last 15 minutes.

        In a live system you'd probably want to rate-limit this.

        :return: Price in Pence
        :rtype int:
        """
        ts_fifteen_minutes_ago = time.time() - 900

        total_price_times_quantity = 0
        total_quantity = 0

        for trade in reversed(self.trades):
            # Loop through the trades list in reverse until we get to trades older than 15 minutes ago
            if trade.timestamp < ts_fifteen_minutes_ago:
                break

            total_price_times_quantity += trade.price * trade.quantity
            total_quantity += trade.quantity

        if total_quantity > 0:
            return total_price_times_quantity / total_quantity

        else:  # No recent trades, return par value just as a sensible default
            return self.par_value


    def calculate_price_to_earnings_ratio(self):
        """
        Calculate the price to earnings ratio. This is the stock price / dividend yield.
        :return:
        :rtype float:
        """
        return self.calculate_price() / self.calculate_dividend_yield()



class CommonStock(Stock):
    """
    A standard stock with standard dividends
    """
    type = Stock.TYPE_COMMON

    def calculate_dividend_yield(self):
        """
        For Common Stocks this is just the last dividend / stock price
        :return:
        """
        return self.last_dividend / self.calculate_price()


class PreferredStock(Stock):
    """
    PreferredStocks differ from CommonStocks by having a fixed dividend rate which is a percentage of the par value,
    which effects how the dividend yield is calculated.
    """
    type = Stock.TYPE_PREFERRED

    def __init__(self, symbol, par_value, last_dividend, fixed_dividend_percent):
        super(PreferredStock, self).__init__(symbol, par_value, last_dividend)

        # fixed dividend is a percentage value
        assert 0.0 <= fixed_dividend_percent <= 1.0

        self.fixed_dividend = fixed_dividend_percent

    def calculate_dividend_yield(self):
        """
        For Preferred Stocks this is calculated as the fixed dividend * par_value / stock price
        :return:
        """
        return (self.fixed_dividend * self.par_value) / self.calculate_price()