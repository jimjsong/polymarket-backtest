import pandas as pd
import numpy as np

def generate_dummy_data(n=1000):
    # Simulate a price path
    np.random.seed(42)
    prices = [0.5]
    for _ in range(n):
        change = np.random.normal(0, 0.01)
        new_price = prices[-1] + change
        new_price = max(0.01, min(0.99, new_price))
        prices.append(new_price)

    timestamps = pd.date_range(start='2024-01-01', periods=n+1, freq='15min').astype(int) // 10**9

    df = pd.DataFrame({
        'timestamp': timestamps,
        'price': prices,
        'size': np.random.randint(10, 1000, n+1),
        'side': ['buy'] * (n+1) # dummy
    })
    return df
