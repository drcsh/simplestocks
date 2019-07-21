import unittest, time
from unittest import mock

from stock import Stock, CommonStock, PreferredStock
from trade import Trade


class StockTests(object):
    """
        Non standalone tests for functions common to all kinds of Stocks.

        Override the class variables in child test cases.
    """
    stock_dividend_0 = None
    stock_dividend_5 = None

    def set_up_trades(self):
        self.trade_100_at_500 = Trade(time.time() - 60, 100, Trade.BUY_INDICATOR, 500)
        self.trade_100_at_1000 = Trade(time.time() - 60, 100, Trade.BUY_INDICATOR, 1000)

        self.trade_100_at_100 = Trade(time.time() - 60, 100, Trade.BUY_INDICATOR, 100)
        self.trade_100_at_105 = Trade(time.time() - 55, 100, Trade.SELL_INDICATOR, 105)
        self.trade_100_at_110 = Trade(time.time() - 50, 100, Trade.BUY_INDICATOR, 110)

        self.old_trade = Trade(time.time() - 10000, 999, Trade.BUY_INDICATOR, 1000)

        self.no_trades = []
        self.one_trade_at_500 = [self.trade_100_at_500]
        self.one_trade_at_500_and_old_trade = [self.old_trade, self.trade_100_at_500]
        self.three_trades = [self.trade_100_at_100, self.trade_100_at_105, self.trade_100_at_110]

    def test_record_trade_basic(self):
        # Base case, add a trade when there are none
        self.stock_dividend_0.trades = self.no_trades
        self.stock_dividend_0.record_trade(self.trade_100_at_100)

        last_trade = self.stock_dividend_0.trades[-1]

        self.assertEqual(len(self.stock_dividend_0.trades), 1)
        self.assertEqual(last_trade, self.trade_100_at_100)

    def test_record_trade_bad_trade(self):
        # Edge case: nonsense given raises an exception
        self.assertRaises(TypeError, self.stock_dividend_0.record_trade, trade="I am a string, not a trade!")

    def test_record_trade_multiple(self):
        # Test adding a few and getting them back in the right order
        self.stock_dividend_5.trades = self.no_trades

        self.stock_dividend_5.record_trade(self.trade_100_at_100)
        self.stock_dividend_5.record_trade(self.trade_100_at_110)

        last_trade = self.stock_dividend_5.trades[-1]
        second_last_trade = self.stock_dividend_5.trades[-2]

        self.assertEqual(len(self.stock_dividend_5.trades), 2)
        self.assertEqual(last_trade, self.trade_100_at_110)
        self.assertEqual(second_last_trade, self.trade_100_at_100)


    def test_calculate_price_basic(self):
        # Easy case, one trade at 500
        self.stock_dividend_0.trades = self.one_trade_at_500
        self.assertEqual(self.stock_dividend_0.calculate_price(), 500)

    def test_calculate_price_default(self):
        # Base case, no trades, returns par value
        self.stock_dividend_0.trades = self.no_trades
        self.assertEqual(self.stock_dividend_0.calculate_price(), self.stock_dividend_0.par_value)

    def test_calculate_price_time_cutoff(self):
        # Old trades should get ignored
        self.stock_dividend_0.trades = self.one_trade_at_500_and_old_trade
        self.assertEqual(self.stock_dividend_0.calculate_price(), 500)

    def test_calculate_price_realistic(self):
        # Check that something resembling actual trades works
        self.stock_dividend_0.trades = self.three_trades

        expected_price = 105  # ((100*100)+(100*105)+(100*110)) / 300 = 105
        self.assertEqual(self.stock_dividend_0.calculate_price(), expected_price)

    def test_p_to_e_ratio_basic(self):
        # basic test that we can work out a p/e ratio with a stock price of 100 and a last dividend of 5
        with mock.patch.object(Stock, 'calculate_price', return_value=100):
            self.assertEqual(self.stock_dividend_5.calculate_price_to_earnings_ratio(), 20)

    def test_p_to_e_ratio_with_zero_dividend(self):
        # make sure that we don't do a div/0
        with mock.patch.object(Stock, 'calculate_price', return_value=100):
            self.assertEqual(self.stock_dividend_0.calculate_price_to_earnings_ratio(), 0)

class TestCommonStock(unittest.TestCase, StockTests):

    def setUp(self):

        self.stock_dividend_0 = CommonStock("TE0", 100, 0)
        self.stock_dividend_5 = CommonStock("TE5", 100, 5)

        self.set_up_trades()

    def test_dividend_yield_basic(self):
        # Set the calculated price to 500
        with mock.patch.object(Stock, 'calculate_price', return_value=500):

            # common stock dividend 5, value = 500 yield = 0.01
            self.assertEqual(self.stock_dividend_5.calculate_dividend_yield(), 0.01)

    def test_dividend_yield_zero(self):
        # Set the calculated price to 500
        with mock.patch.object(Stock, 'calculate_price', return_value=500):
            # common stock dividend 0
            self.assertEqual(self.stock_dividend_0.calculate_dividend_yield(), 0)


class TestPreferredStock(unittest.TestCase, StockTests):

    def setUp(self):

        # Set up stocks for shared tests. Note the fixed dividend rates are set to check that these do not impact
        # common functions
        self.stock_dividend_0 = PreferredStock("TE0", 100, 0, 0.2)
        self.stock_dividend_5 = PreferredStock("TE5", 100, 5, 0.3)

        self.stock_f_dividend_5 = PreferredStock("TE5", 100, 0, 0.05)
        self.stock_f_dividend_0 = PreferredStock("TE0", 100, 0, 0)

        self.set_up_trades()

    def test_dividend_yield_basic(self):
        # Set the calculated price to 100 for testing
        with mock.patch.object(PreferredStock, 'calculate_price', return_value=100):

            # 0 fixed dividend = 0 yield
            self.assertEqual(self.stock_f_dividend_0.calculate_dividend_yield(), 0)

    def test_dividend_yield_zero(self):
        # Set the calculated price to 100 for testing
        with mock.patch.object(PreferredStock, 'calculate_price', return_value=100):
            # 5 fixed dividend % * par value 100 / stock price 100 = 0.05 yield
            self.assertEqual(self.stock_f_dividend_5.calculate_dividend_yield(), 0.05)


if __name__ == '__main__':
    unittest.main()