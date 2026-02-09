import unittest
import pandas as pd
from src.backtester import Backtester
from src.strategy import SimpleStrategy

class TestBacktester(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame
        self.data = pd.DataFrame({
            'timestamp': [1, 2, 3, 4, 5],
            'price': [0.5, 0.45, 0.35, 0.30, 0.40],
            'size': [100, 100, 100, 100, 100],
            'side': ['buy', 'sell', 'buy', 'sell', 'buy']
        })
        self.strategy = SimpleStrategy(buy_threshold=0.40, sell_threshold=0.60)
        self.backtester = Backtester(self.data, self.strategy, initial_balance=1000)

    def test_run(self):
        results = self.backtester.run()

        # Check basic output structure
        self.assertIn('final_equity', results)
        self.assertIn('roi', results)
        self.assertIn('trades', results)
        self.assertIn('equity_curve', results)

        # Check if trades were executed
        # At index 2 (price=0.35), buy signal.
        # At index 3 (price=0.30), buy signal (but maybe we already hold position? Strategy generates BUY again).
        # Our simple backtester buys more if it can afford.
        # But wait, my implementation of `_buy` checks max risk per trade. It allows multiple buys.

        trades = results['trades']
        self.assertFalse(trades.empty, "Should have executed trades")

        # Check if equity curve exists
        equity_curve = results['equity_curve']
        self.assertEqual(len(equity_curve), len(self.data))

if __name__ == '__main__':
    unittest.main()
