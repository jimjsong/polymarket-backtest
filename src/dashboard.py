import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_performance(backtest_results, save_path=None):
    """
    Plots the equity curve and trade markers.
    """
    equity_curve = backtest_results.get('equity_curve', pd.DataFrame())
    trades = backtest_results.get('trades', pd.DataFrame())

    if equity_curve.empty:
        print("No equity curve to plot.")
        return

    plt.figure(figsize=(12, 6))

    # Plot equity
    # Convert timestamp to datetime if numeric
    timestamps = pd.to_datetime(equity_curve['timestamp'], unit='s')
    plt.plot(timestamps, equity_curve['equity'], label='Equity', color='blue')

    # Plot buy/sell markers
    if not trades.empty:
        buys = trades[trades['type'] == 'BUY']
        sells = trades[trades['type'] == 'SELL']

        buy_times = pd.to_datetime(buys['timestamp'], unit='s')
        sell_times = pd.to_datetime(sells['timestamp'], unit='s')

        # Create a lookup series
        # Ensure unique index
        equity_curve_unique = equity_curve.drop_duplicates(subset='timestamp')
        equity_series = equity_curve_unique.set_index('timestamp')['equity']

        def get_equity(ts):
            val = equity_series.get(ts)
            if val is None:
                # If timestamp mismatch, return first equity (fallback)
                return equity_series.iloc[0]
            if isinstance(val, (pd.Series, np.ndarray, list)):
                # If duplicates still exist (shouldn't with drop_duplicates), take first
                return val.iloc[0] if hasattr(val, 'iloc') else val[0]
            return val

        buy_equities = [get_equity(ts) for ts in buys['timestamp']]
        sell_equities = [get_equity(ts) for ts in sells['timestamp']]

        plt.scatter(buy_times, buy_equities, marker='^', color='green', label='Buy', s=100, zorder=5)
        plt.scatter(sell_times, sell_equities, marker='v', color='red', label='Sell', s=100, zorder=5)

    plt.title('Backtest Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Equity ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

def print_summary(results):
    print("\nBacktest Summary")
    print("=" * 30)
    print(f"Final Equity:   ${results['final_equity']:,.2f}")
    print(f"ROI:            {results['roi']:.2f}%")
    print(f"Win Rate:       {results['win_rate']:.2f}%")
    print(f"Max Drawdown:   {results['max_drawdown']:.2f}%")
    trades = results.get('trades', [])
    print(f"Total Trades:   {len(trades)}")
    print("=" * 30)
