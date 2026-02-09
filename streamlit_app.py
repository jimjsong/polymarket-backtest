import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.backtester import Backtester
from src.strategy import SimpleStrategy, MovingAverageCrossover
from src.utils import generate_dummy_data

def plot_performance(backtest_results):
    equity_curve = backtest_results.get('equity_curve', pd.DataFrame())
    trades = backtest_results.get('trades', pd.DataFrame())

    if equity_curve.empty:
        st.warning("No equity curve to plot.")
        return None

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot equity
    # Convert timestamp to datetime if numeric
    timestamps = pd.to_datetime(equity_curve['timestamp'], unit='s')
    ax.plot(timestamps, equity_curve['equity'], label='Equity', color='blue')

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

        ax.scatter(buy_times, buy_equities, marker='^', color='green', label='Buy', s=100, zorder=5)
        ax.scatter(sell_times, sell_equities, marker='v', color='red', label='Sell', s=100, zorder=5)

    ax.set_title('Backtest Equity Curve')
    ax.set_xlabel('Date')
    ax.set_ylabel('Equity ($)')
    ax.legend()
    ax.grid(True)
    return fig

st.title("Polymarket Backtester")

if 'results' not in st.session_state:
    st.session_state.results = None
if 'df' not in st.session_state:
    st.session_state.df = None

st.sidebar.header("Configuration")

# Data Source
data_source = st.sidebar.selectbox("Data Source", ["Dummy Data", "Upload CSV"])

if data_source == "Dummy Data":
    n_points = st.sidebar.number_input("Number of Data Points", min_value=100, max_value=10000, value=1000)
    if st.sidebar.button("Generate Data"):
        st.session_state.df = generate_dummy_data(n_points)
        st.success(f"Generated {len(st.session_state.df)} data points.")
elif data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(st.session_state.df)} rows.")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")

# Strategy Selection
strategy_name = st.sidebar.selectbox("Select Strategy", ["Simple Strategy", "Moving Average Crossover"])
strategy = None

if strategy_name == "Simple Strategy":
    buy_threshold = st.sidebar.slider("Buy Threshold", 0.0, 1.0, 0.45)
    sell_threshold = st.sidebar.slider("Sell Threshold", 0.0, 1.0, 0.55)
    strategy = SimpleStrategy(buy_threshold=buy_threshold, sell_threshold=sell_threshold)
elif strategy_name == "Moving Average Crossover":
    short_window = st.sidebar.number_input("Short Window", min_value=1, value=5)
    long_window = st.sidebar.number_input("Long Window", min_value=2, value=20)
    strategy = MovingAverageCrossover(short_window=short_window, long_window=long_window)

# Run Backtest
if st.sidebar.button("Run Backtest"):
    if st.session_state.df is None:
        # Generate dummy data if not loaded, respecting n_points if in Dummy Data mode
        if data_source == "Dummy Data":
             st.session_state.df = generate_dummy_data(n_points)
        else:
            st.error("Please load data first.")
            st.stop()

    if strategy:
        backtester = Backtester(st.session_state.df, strategy)
        st.session_state.results = backtester.run()

# Display Results
if st.session_state.results:
    st.subheader("Backtest Results")
    results = st.session_state.results

    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Final Equity", f"${results['final_equity']:,.2f}")
    col2.metric("ROI", f"{results['roi']:.2f}%")
    col3.metric("Win Rate", f"{results['win_rate']:.2f}%")
    col4.metric("Max Drawdown", f"{results['max_drawdown']:.2f}%")

    # Plot
    fig = plot_performance(results)
    if fig:
        st.pyplot(fig)

    # Trade History
    with st.expander("Trade History"):
        st.dataframe(results['trades'])
