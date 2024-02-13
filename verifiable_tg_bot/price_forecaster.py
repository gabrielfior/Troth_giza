import dataclasses
import pandas as pd
import matplotlib.pyplot as plt
import polars
import prophet
from prophet import Prophet
from giza_datasets import DatasetsLoader

@dataclasses.dataclass
class PriceForecaster:

    loader: DatasetsLoader

    def __init__(self):
        self.loader = DatasetsLoader()

    def fetch_4h_eth_price_last_30_days(self):
        df : polars.DataFrame = self.loader.load('tokens-daily-prices-mcap-volume')
        #df["date"] = pd.to_datetime(df["date"], unit="ms")
        pd.to_datetime(df['date'])
        df: pd.DataFrame = df.to_pandas()
        df.set_index("date", inplace=True)
        return df

    def forecast(self, df: pd.DataFrame, days_for_forecast = 5, token = 'ETH'):
        available_tokens = df['token'].unique()
        if token not in available_tokens:
            raise ValueError(f"token not available, must be contained in {available_tokens}")
        df = df[df['token'] == token]
        data = df[["price"]].reset_index().rename(columns={"price": "y", "date": "ds"})
        # We only take last 100 days for easier plotting
        data = data[-100:]
        #m = Prophet(seasonality_mode='multiplicative').fit(data)
        m = Prophet().fit(data)
        future = m.make_future_dataframe(periods=int(days_for_forecast),
                                         freq='d')  # 1 period == 4h, 5 days == 5*24/4
        prediction = m.predict(future)

        last_date = data.iloc[-1].ds
        fig = self.build_fig(prediction, last_date, m, token, days_for_forecast)
        return fig

    def build_fig(self, prediction: pd.DataFrame, last_date: pd.Timestamp,
                  model: prophet.forecaster.Prophet, token: str, days_for_forecast: int):
        fig, ax = plt.subplots()
        fig = model.plot(prediction, ax, include_legend=True)
        plt.title(f"Prediction of ETH Price over next {days_for_forecast} days")
        ax.set_xlabel("Date")
        plt.axvline(x=last_date, color='g', linestyle='--', label='Cutoff')
        # plt.vlines([1,2,3], 0, 1, label='test')
        plt.legend()
        plt.tight_layout()
        ax.set_xticks(ax.get_xticks()[::2])
        ax.set_ylabel(f"Close {token} price (USD)")
        return fig