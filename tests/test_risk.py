import unittest
import pandas as pd
from src.backtester import Backtester
from src.strategy import SimpleStrategy

class TestRisk(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'timestamp': [1, 2],
            'price': [0.5, 0.5],
            'size': [100, 100],
            'side': ['buy', 'buy']
        })
        self.strategy = SimpleStrategy(buy_threshold=0.6, sell_threshold=0.8) # Always BUY
        self.initial_balance = 1000
        self.backtester = Backtester(self.data, self.strategy, initial_balance=self.initial_balance)
        self.backtester.max_portfolio_risk_per_trade = 0.10 # 10%
        self.backtester.slippage_pct = 0.0 # Simplify calc

    def test_max_trade_size(self):
        # First trade
        self.backtester.run()
        trades = self.backtester.trade_history
        first_trade = trades[0]

        # Max trade value should be 10% of 1000 = 100
        # Price is 0.5
        # Quantity should be 100 / 0.5 = 200

        expected_cost = 100.0
        self.assertAlmostEqual(first_trade['cost'], expected_cost, delta=1.0)
        self.assertEqual(first_trade['type'], 'BUY')

        # Check balance after trade: 1000 - 100 = 900
        self.assertAlmostEqual(first_trade['balance'], 900.0, delta=1.0)

if __name__ == '__main__':
    unittest.main()
