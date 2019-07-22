import unittest
from unittest import mock

from exchange import Exchange, InvalidStockException
from trade import Trade


def quick_mock_stock(price):
    """
    Sets up a Mock to be used as a stand in for a stock

    :param int price: value to be returned from calculate_price
    :return:
    """
    stock = mock.Mock()
    stock.calculate_price.return_value = price
    return stock


class test_exchange(unittest.TestCase):
    """
    Test the Exchange object which handles transactions and exchange level info
    """

    def setUp(self):

        self.stock_100 = quick_mock_stock(100)
        self.stock_105 = quick_mock_stock(105)
        self.stock_110 = quick_mock_stock(110)
        self.stock_200 = quick_mock_stock(200)

        # basic stocks and exchange combo for tests
        self.basic_stocks = {
            "100": self.stock_100,
            "105": self.stock_105
        }
        self.basic_exchange = Exchange("TESTEX", self.basic_stocks)

    def test_get_stock_basic(self):
        # check we get the right stock if we ask for it
        self.assertEqual(self.basic_exchange.get_stock("105"), self.stock_105)

    def test_get_stock_does_not_exist(self):
        # edge case: check we get an appropriate exception for bad input
        self.assertRaises(InvalidStockException, self.basic_exchange.get_stock, stock_symbol='DOESNOTEXIST')

    def test_buy_stock(self):
        with mock.patch.object(self.stock_100, 'record_trade') as mockstock:
            self.basic_exchange.buy_stock("100", 200, 100)

            mockstock.assert_called_once()

            trade = mockstock.call_args[0][0]

            self.assertEqual(trade.quantity, 200)
            self.assertEqual(trade.price, 100)
            self.assertEqual(trade.indicator, Trade.BUY_INDICATOR)

    def test_sell_stock(self):
        with mock.patch.object(self.stock_105, 'record_trade') as mockstock:
            self.basic_exchange.sell_stock("105", 200, 99)

            mockstock.assert_called_once()

            trade = mockstock.call_args[0][0]

            self.assertEqual(trade.quantity, 200)
            self.assertEqual(trade.price, 99)
            self.assertEqual(trade.indicator, Trade.SELL_INDICATOR)

    def test_all_share_index_basic(self):
        # basic test case, 1 stock of value 100, means the index value is 100
        exchange = Exchange("TESTEX", {"100": self.stock_100})
        all_share_index = exchange.calculate_all_share_index()

        self.assertEqual(all_share_index, 100)

    def test_all_share_index_empty(self):
        # Edge case, no stocks
        exchange = Exchange("TESTEX", {})
        all_share_index = exchange.calculate_all_share_index()

        self.assertEqual(all_share_index, 0)

    def test_all_share_index_realistic(self):
        # More realistic case, spread of stock values
        stocks = {"100": self.stock_100,
                  "105": self.stock_105,
                  "110": self.stock_110,
                  "200": self.stock_200
                  }
        exchange = Exchange("TESTEX", stocks)
        all_share_index = exchange.calculate_all_share_index()

        self.assertAlmostEqual(all_share_index, 123.283, places=3)  # note rounding.
