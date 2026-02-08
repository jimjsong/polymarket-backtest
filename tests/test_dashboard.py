import unittest
import pandas as pd
import os
from polymarket_backtester.src.dashboard import plot_performance

class TestDashboard(unittest.TestCase):
    def test_plot_performance(self):
        # Create dummy results
        equity_curve = pd.DataFrame({
            'timestamp': [1609459200, 1609462800, 1609466400],
            'equity': [1000, 1050, 1100]
        })
        trades = pd.DataFrame({
            'timestamp': [1609462800],
            'type': ['BUY'],
            'price': [0.5],
            'quantity': [100]
        })
        results = {
            'equity_curve': equity_curve,
            'trades': trades
        }
        
        save_path = "test_plot.png"
        if os.path.exists(save_path):
            os.remove(save_path)
            
        plot_performance(results, save_path=save_path)
        
        self.assertTrue(os.path.exists(save_path))
        os.remove(save_path)

if __name__ == '__main__':
    unittest.main()
