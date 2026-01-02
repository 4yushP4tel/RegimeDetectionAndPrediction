from datetime import datetime
from typing import Optional
import pandas as pd
import numpy as np
import websocket
import threading
import asyncio
import requests
from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.live import StockDataStream, OptionDataStream
from alpaca.data.requests import StockBarsRequest, OptionBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.timeframe import TimeFrameUnit
from dotenv import load_dotenv
import os

load_dotenv()
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET_KEY = os.getenv("ALPACA_API_SECRET_KEY")

class DataPipeLine:
    """
    Using XLK as the tech sector etf
    """

    # these holdings could be used to find the correlation structure
    # which could be used as an endogenous feature in HMM
    TOP_HOLDINGS_XLK = ["NVDA", "AAPL", "MSFT", "AVGO", "PLTR", "AMD", "ORCL",
                        "MU", "CSCO", "IBM"]
    
    COL_ORDER = ["date","close","open","high","low","volume"]
    TRAINING_COLS = []
    def __init__(self):
        self.client = None
        self.stream = None
        self.connect_to_alpaca()

    def connect_to_alpaca(self):
        try:
            self.client = StockHistoricalDataClient(api_key=ALPACA_API_KEY, secret_key=ALPACA_API_SECRET_KEY)
            self.stream = StockDataStream(api_key=ALPACA_API_KEY, secret_key=ALPACA_API_SECRET_KEY)
        except Exception as e:
            print(f"Error connecting to Alpace: {e}")

    def fetch_historical_data(self, symbol: str, start_date: Optional[datetime]=None, end_date: Optional[datetime]=None) -> pd.DataFrame:
        try:
            response = self.client.get_stock_bars(StockBarsRequest(symbol_or_symbols=symbol, 
                                              timeframe=TimeFrame(1, TimeFrameUnit.Day),
                                              start=start_date,
                                              end=end_date))
            df = response.df
            print(f"Response df for {symbol}: \n {df}")
            df["date"] = df.index.get_level_values(1).strftime("%Y-%m-%d")
            df.reset_index(drop=True, inplace=True)
            df = df[self.COL_ORDER]
            return df
        except Exception as e:
            print(f"Error fetching historical data: {e}")

    def fetch_full_historical_data(self, symbol: str) -> pd.DataFrame:
        return self.fetch_historical_data(symbol, datetime(1900,1,1))

    def fetch_live_data(self):
        try:
            pass
        except Exception as e:
            print(f"Error fetching live data: {e}")
        
    def fetch_and_transform_holdings_data(self) -> pd.DataFrame:
        df_mapping = {}
        for holding in self.TOP_HOLDINGS_XLK:
            temp_df = self.fetch_full_historical_data(holding)
            temp_df = temp_df.set_index("date")
            DataPipeLine._get_log_returns(temp_df)
            print(f"Here is the data for : {holding}\n {temp_df}")
            print()
            df_mapping[holding] = temp_df
        
        combined_log_returns_df = pd.concat(df_mapping, axis=1, ignore_index=True)
        return combined_log_returns_df

    def compute_correlation_matrix_of_holdings(self, log_returns_df: pd.DataFrame):
        pass

    @staticmethod
    def _get_log_returns(df: pd.DataFrame):
        #using the close prices for this
        df["log_returns"] = np.log(df["close"]/df["close"].shift(1))
        df.dropna(inplace=True)

    @staticmethod
    def _get_intraday_price_range(df: pd.DataFrame):
        df["price_range"] = abs(df["high"] - df["low"])

    @staticmethod
    def _get_rolling_stats(df: pd.DataFrame):
        pass

    @staticmethod
    def get_training_data(df):
        DataPipeLine._get_intraday_price_range(df)
        DataPipeLine._get_log_returns(df)

    def get_implied_vol(self):
        """
        Check if there is some api which offers histoical options data
        """
        pass

    def get_VIX(self):
        pass
    
    @staticmethod
    def save_data_to_csv(df: pd.DataFrame, file_name:str):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', file_name))
        df.to_csv(file_path, index=False)

    @staticmethod
    def save_data_to_existing_csv(df: pd.DataFrame, file_name:str):
        file_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', file_name))
        print(f"Saving data to existing csv at {file_abs_path}")
        old_df = pd.read_csv(file_abs_path)
        df = pd.concat([old_df, df], axis= 0, ignore_index=True)
        df.drop_duplicates(subset=["date"], inplace=True)
        df.sort_values(by="date", inplace=True)
        df.to_csv(file_abs_path, index=False)

    @staticmethod
    def change_csv_date_format(file_name:str):
        # used for the data which I got online
        file = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
        df = pd.read_csv(file)
        df["date"] = df["date"].str.split("T").str[0]
        df.reset_index(drop=True, inplace=True)
        df.to_csv(file, index=False)

if __name__ == "__main__":
    dp = DataPipeLine()
    dp.fetch_and_transform_holdings_data()