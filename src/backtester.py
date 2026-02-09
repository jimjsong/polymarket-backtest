import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, data, strategy, initial_balance=10000):
        self.data = data.reset_index(drop=True)
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.position_size = 0.0 # Number of contracts
        self.avg_buy_price = 0.0 # Weighted average entry price
        self.trade_history = []
        self.equity_curve = []

        # Risk management parameters
        self.max_portfolio_risk_per_trade = 0.10 # 10%
        self.slippage_pct = 0.01 # 1% default
        self.fee_pct = 0.00

    def run(self):
        """
        Iterates through the data and executes trades based on strategy signals.
        Returns:
            dict: Summary of backtest results.
        """
        self.equity_curve = []
        self.trade_history = []
        self.current_balance = self.initial_balance
        self.position_size = 0.0
        self.avg_buy_price = 0.0

        for i in range(len(self.data)):
            row = self.data.iloc[i]
            history_slice = self.data.iloc[:i+1]
            signal = self.strategy.generate_signal(row, history_slice)

            self._execute_signal(signal, row)
            self._update_equity(row)

        return self._generate_report()

    def _execute_signal(self, signal, row):
        price = row['price']
        timestamp = row['timestamp']

        if signal == 'BUY':
            self._buy(price, timestamp)
        elif signal == 'SELL':
            self._sell(price, timestamp)

    def _buy(self, price, timestamp):
        # 10% of current equity
        current_equity = self._calculate_equity(price)
        max_trade_value = current_equity * self.max_portfolio_risk_per_trade

        # Slippage: Buying higher
        execution_price = price * (1 + self.slippage_pct)
        if execution_price <= 0: return

        # Calculate quantity
        affordable_amount = min(max_trade_value, self.current_balance)
        quantity = affordable_amount / execution_price

        if quantity > 0:
            cost = quantity * execution_price
            fee_amount = cost * self.fee_pct
            total_cost = cost + fee_amount

            if total_cost <= self.current_balance:
                # Update weighted average buy price
                total_position_value = (self.position_size * self.avg_buy_price) + (quantity * execution_price)
                new_position_size = self.position_size + quantity
                self.avg_buy_price = total_position_value / new_position_size if new_position_size > 0 else 0.0

                self.current_balance -= total_cost
                self.position_size = new_position_size

                self.trade_history.append({
                    'timestamp': timestamp,
                    'type': 'BUY',
                    'price': execution_price,
                    'quantity': quantity,
                    'cost': total_cost,
                    'balance': self.current_balance
                })

    def _sell(self, price, timestamp):
        if self.position_size > 0:
            # Slippage: Selling lower
            execution_price = price * (1 - self.slippage_pct)
            if execution_price <= 0: execution_price = 0.0001

            revenue = self.position_size * execution_price
            fee_amount = revenue * self.fee_pct
            net_revenue = revenue - fee_amount

            # Calculate PnL for this trade (round trip)
            pnl = (execution_price - self.avg_buy_price) * self.position_size
            pnl_pct = (pnl / (self.avg_buy_price * self.position_size)) if self.avg_buy_price > 0 else 0.0

            self.current_balance += net_revenue
            self.trade_history.append({
                'timestamp': timestamp,
                'type': 'SELL',
                'price': execution_price,
                'quantity': self.position_size,
                'revenue': net_revenue,
                'balance': self.current_balance,
                'pnl': pnl,
                'pnl_pct': pnl_pct
            })

            self.position_size = 0.0
            self.avg_buy_price = 0.0

    def _calculate_equity(self, current_price):
        position_value = self.position_size * current_price
        return self.current_balance + position_value

    def _update_equity(self, row):
        current_price = row['price']
        total_equity = self._calculate_equity(current_price)
        self.equity_curve.append({
            'timestamp': row['timestamp'],
            'equity': total_equity
        })

    def _generate_report(self):
        df_trades = pd.DataFrame(self.trade_history)
        df_equity = pd.DataFrame(self.equity_curve)

        final_equity = df_equity.iloc[-1]['equity'] if not df_equity.empty else self.initial_balance
        roi = ((final_equity - self.initial_balance) / self.initial_balance) * 100

        win_rate = 0.0
        if not df_trades.empty and 'pnl' in df_trades.columns:
            closed_trades = df_trades[df_trades['type'] == 'SELL']
            if not closed_trades.empty:
                winning_trades = closed_trades[closed_trades['pnl'] > 0]
                win_rate = (len(winning_trades) / len(closed_trades)) * 100

        # Max Drawdown
        max_drawdown = 0.0
        if not df_equity.empty:
            equity_series = df_equity['equity']
            peak = equity_series.cummax()
            drawdown = (equity_series - peak) / peak
            max_drawdown = drawdown.min() * 100 # In percentage (negative)

        return {
            'final_equity': final_equity,
            'roi': roi,
            'trades': df_trades,
            'equity_curve': df_equity,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown
        }
