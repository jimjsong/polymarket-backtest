import unittest
import pandas as pd
from polymarket_backtester.src.strategy import SimpleStrategy, MovingAverageCrossover

class TestStrategy(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame
        self.data = pd.DataFrame({
            'timestamp': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'price': [0.5, 0.45, 0.35, 0.30, 0.40, 0.50, 0.60, 0.70, 0.65, 0.55],
            'size': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        })
        
    def test_simple_strategy(self):
        strategy = SimpleStrategy(buy_threshold=0.40, sell_threshold=0.60)
        
        # Test BUY signal (price=0.35)
        row = self.data.iloc[2]
        signal = strategy.generate_signal(row)
        self.assertEqual(signal, 'BUY')
        
        # Test SELL signal (price=0.65)
        row = self.data.iloc[8]
        signal = strategy.generate_signal(row)
        self.assertEqual(signal, 'SELL')
        
        # Test HOLD signal (price=0.50)
        row = self.data.iloc[5]
        signal = strategy.generate_signal(row)
        self.assertEqual(signal, 'HOLD')
        
    def test_ma_strategy(self):
        strategy = MovingAverageCrossover(short_window=3, long_window=5)
        
        # Simulate moving through the data
        # At index 4 (price=0.40), history=[0.5, 0.45, 0.35, 0.30, 0.40]
        # short_ma (last 3): (0.35+0.30+0.40)/3 = 0.35
        # long_ma (last 5): (0.5+0.45+0.35+0.30+0.40)/5 = 0.40
        # short < long => SELL
        
        history = self.data.iloc[:5]
        row = self.data.iloc[4]
        signal = strategy.generate_signal(row, history)
        self.assertEqual(signal, 'SELL')
        
        # At index 7 (price=0.70), history=[..., 0.30, 0.40, 0.50, 0.60, 0.70]
        # short_ma (last 3): (0.50+0.60+0.70)/3 = 0.60
        # long_ma (last 5): (0.30+0.40+0.50+0.60+0.70)/5 = 0.50
        # short > long => BUY
        
        history = self.data.iloc[:8]
        row = self.data.iloc[7]
        signal = strategy.generate_signal(row, history)
        self.assertEqual(signal, 'BUY')

if __name__ == '__main__':
    unittest.main()
