import unittest
import pandas as pd
from src.sweeper import ParameterSweeper
from src.strategy import SimpleStrategy

class TestSweeper(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'timestamp': [1, 2, 3],
            'price': [0.5, 0.45, 0.55],
            'size': [100, 100, 100],
            'side': ['buy', 'sell', 'buy']
        })
        self.param_grid = {
            'buy_threshold': [0.40, 0.50],
            'sell_threshold': [0.60, 0.70]
        }

    def test_sweep(self):
        sweeper = ParameterSweeper(self.data, SimpleStrategy, self.param_grid)
        df = sweeper.run()

        # 2 * 2 = 4 combinations
        self.assertEqual(len(df), 4)

        # Check columns
        self.assertIn('params', df.columns)
        self.assertIn('roi', df.columns)

        # Check best result
        best = sweeper.best_result()
        self.assertIsNotNone(best)

if __name__ == '__main__':
    unittest.main()
