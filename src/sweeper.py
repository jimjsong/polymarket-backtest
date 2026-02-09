import itertools
import pandas as pd
from .backtester import Backtester

class ParameterSweeper:
    def __init__(self, data, strategy_class, param_grid):
        """
        Args:
            data (pd.DataFrame): Data to backtest on.
            strategy_class (class): The strategy class to instantiate.
            param_grid (dict): Dictionary of parameter names and lists of values.
        """
        self.data = data
        self.strategy_class = strategy_class
        self.param_grid = param_grid
        self.results = []

    def run(self):
        keys = self.param_grid.keys()
        values = self.param_grid.values()
        combinations = list(itertools.product(*values))

        print(f"Running sweep with {len(combinations)} combinations...")

        for combo in combinations:
            params = dict(zip(keys, combo))
            # Instantiate strategy with params
            try:
                strategy = self.strategy_class(**params)

                backtester = Backtester(self.data, strategy)
                result = backtester.run()

                # Store summary
                summary = {
                    'params': params,
                    'final_equity': result['final_equity'],
                    'roi': result['roi'],
                    'win_rate': result['win_rate'],
                    'max_drawdown': result['max_drawdown'],
                    'trades_count': len(result['trades'])
                }
                self.results.append(summary)
            except Exception as e:
                print(f"Error running backtest with params {params}: {e}")

        return pd.DataFrame(self.results)

    def best_result(self, metric='roi'):
        if not self.results:
            return None
        df = pd.DataFrame(self.results)
        return df.sort_values(by=metric, ascending=False).iloc[0]
