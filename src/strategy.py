import pandas as pd

class Strategy:
    def __init__(self, name="BaseStrategy"):
        self.name = name

    def generate_signal(self, row, history_df=None):
        """
        Generates a trading signal for a given data row.
        Args:
            row (pd.Series): The current data row (timestamp, price, etc.).
            history_df (pd.DataFrame): The historical data up to this point (including current row).
        Returns:
            str: 'BUY', 'SELL', or 'HOLD'.
        """
        raise NotImplementedError("Strategy must implement generate_signal method.")

class SimpleStrategy(Strategy):
    def __init__(self, buy_threshold=0.40, sell_threshold=0.60, volume_threshold=0):
        super().__init__(name="SimpleThresholdStrategy")
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.volume_threshold = volume_threshold

    def generate_signal(self, row, history_df=None):
        price = row['price']
        size = row.get('size', 0)
        
        # Volume filter
        if size < self.volume_threshold:
            return 'HOLD'
            
        # Example logic: Buy if price < buy_threshold, Sell if price > sell_threshold
        if price < self.buy_threshold:
            return 'BUY'
        elif price > self.sell_threshold:
            return 'SELL'
        else:
            return 'HOLD'

class MovingAverageCrossover(Strategy):
    def __init__(self, short_window=5, long_window=20):
        super().__init__(name="MA_Crossover")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, row, history_df=None):
        if history_df is None or len(history_df) < self.long_window:
            return 'HOLD'
        
        # Calculate MAs
        short_ma = history_df['price'].tail(self.short_window).mean()
        long_ma = history_df['price'].tail(self.long_window).mean()
        
        if short_ma > long_ma:
            return 'BUY'
        elif short_ma < long_ma:
            return 'SELL'
        
        return 'HOLD'
