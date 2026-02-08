# Polymarket Backtester

A Python-based backtesting framework for Polymarket's CLOB (Central Limit Order Book) markets, specifically designed for 15-minute event contracts.

## Features

- **Data Downloader**: Fetch historical trade data from Polymarket's CLOB API (`/prices-history`). Includes a `LiveRecorder` to capture order book snapshots for missing history.
- **Strategy Engine**: Modular strategy interface. Includes `SimpleStrategy` (threshold-based) and `MovingAverageCrossover` examples.
- **Execution Simulator**: Realistic backtesting with slippage, fees, and risk management (max 10% portfolio per trade).
- **Analytics Dashboard**: Visualizes equity curve and trade execution points. Calculates ROI, Win Rate, and Max Drawdown.
- **Parameter Sweeper**: Grid search optimization for strategy parameters.

## Structure

- `src/data_downloader.py`: Data fetching and recording.
- `src/strategy.py`: Strategy definitions.
- `src/backtester.py`: Core simulation logic.
- `src/dashboard.py`: Visualization and reporting.
- `src/sweeper.py`: Parameter optimization.
- `main.py`: Entry point for running simulations.
- `tests/`: Unit tests.

## Usage

1. **Install Dependencies**:
   ```bash
   pip install pandas requests matplotlib
   ```

2. **Run the Backtester**:
   Run the main script to execute a backtest with dummy data (default) or configure it to use real data.
   ```bash
   python -m polymarket_backtester.main
   ```

3. **Run Tests**:
   ```bash
   python -m unittest discover polymarket_backtester/tests
   ```

## Configuration

Modify `main.py` to switch between strategies, adjust risk parameters, or change the data source.
To use real data, instantiate `DataDownloader` and fetch data for a specific `token_id`.
