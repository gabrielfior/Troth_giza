import datetime
import io

import matplotlib.pyplot as plt
import pandas as pd
import polars
import prophet
from giza_actions.task import task
from giza_datasets import DatasetsLoader
from prophet import Prophet


class PriceForecaster:
    loader: DatasetsLoader

    def __init__(self):
        self.loader = DatasetsLoader()

    def fetch_4h_eth_price_last_30_days(self):
        df: polars.DataFrame = self.loader.load('tokens-daily-prices-mcap-volume')
        pd.to_datetime(df['date'])
        df: pd.DataFrame = df.to_pandas()
        df.set_index("date", inplace=True)
        return df

    def train_model(self, data):
        m = Prophet().fit(data)
        return m

    def pre_process(self, df: pd.DataFrame, token: str):
        available_tokens = df['token'].unique()
        if token not in available_tokens:
            raise ValueError(f"token not available, must be contained in {available_tokens}")
        df = df[df['token'] == token]
        data = df[["price"]].reset_index().rename(columns={"price": "y", "date": "ds"})
        return data

    def build_fig(self, prediction: pd.DataFrame, last_date: pd.Timestamp,
                  model: prophet.forecaster.Prophet, token: str, days_in_future: int):
        fig, ax = plt.subplots()
        fig = model.plot(prediction, ax, include_legend=True)
        plt.title(f"Prediction of ETH Price over next {days_in_future} days")
        ax.set_xlabel("Date")
        plt.axvline(x=last_date, color='g', linestyle='--', label='Cutoff')
        # plt.vlines([1,2,3], 0, 1, label='test')
        plt.legend()
        plt.tight_layout()
        ax.set_xticks(ax.get_xticks()[::2])
        ax.set_ylabel(f"Close {token} price (USD)")
        return fig

    def forecast(self, df: pd.DataFrame, days_in_future=5, token='ETH'):
        data = self.pre_process(df, token)
        # We only take last 100 days for easier plotting
        data = data[-100:]
        m = self.train_model(data)
        # We forecast 5 days into the future, hence days to be forecasted
        # equal (today + 5days - last_day_from_dataframe)
        diff = datetime.datetime.today() - data.iloc[-1].ds
        days_for_forecast = diff.days + days_in_future
        future = m.make_future_dataframe(periods=int(days_for_forecast),
                                         freq='d')
        prediction = m.predict(future)
        last_date = data.iloc[-1].ds
        fig = self.build_fig(prediction, last_date, m, token, days_in_future)
        return fig

@task(name="do forecast")
def build_fig_for_forecast():
    photo = io.BytesIO()
    pf = PriceForecaster()
    df = pf.fetch_4h_eth_price_last_30_days()
    fig = pf.forecast(df, 5, 'ETH')
    fig.savefig(photo, format='png')
    photo.seek(0)  # to start reading from the beginning. (After writing, the cursor is at the end)
    return photo
