import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.strategy import SimpleStrategy, MovingAverageCrossover
from src.backtester import Backtester
from src.dashboard import plot_performance, print_summary
from src.sweeper import ParameterSweeper
from src.utils import generate_dummy_data

def main():
    print("Starting Polymarket Backtester...")

    # 1. Data Acquisition
    print("Generating dummy data...")
    df = generate_dummy_data()
    print(f"Data loaded: {len(df)} rows")

    # 2. Strategy Definition
    strategy = SimpleStrategy(buy_threshold=0.45, sell_threshold=0.55)

    # 3. Backtesting
    print(f"Running backtest with {strategy.name}...")
    backtester = Backtester(df, strategy)
    results = backtester.run()

    # 4. Analysis
    print_summary(results)
    # plot_performance(results, save_path="backtest_result.png")

    # 5. Parameter Sweep
    print("\nRunning Parameter Sweep...")
    param_grid = {
        'buy_threshold': [0.40, 0.45, 0.48],
        'sell_threshold': [0.52, 0.55, 0.60]
    }
    sweeper = ParameterSweeper(df, SimpleStrategy, param_grid)
    sweep_results = sweeper.run()

    print("\nTop Results:")
    print(sweep_results.sort_values(by='roi', ascending=False).head(5)[['params', 'roi', 'win_rate', 'max_drawdown']])

if __name__ == "__main__":
    main()
