from datetime import datetime
from typing import List, Optional, Tuple
import pandas as pd
import numpy as np
import websocket
import threading
from multiprocessing import Pool, cpu_count
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
    TOP_HOLDINGS_XLK = ["NVDA", "AAPL", "MSFT", "AVGO", "AMD", "ORCL",
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

    def _fetch_historical_data(self, symbol: str, start_date: Optional[datetime]=None, end_date: Optional[datetime]=None) -> pd.DataFrame:
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
        return self._fetch_historical_data(symbol, datetime(1900,1,1))
    
    @staticmethod
    def fetch_historical_data_from_csv(file_name:str = "tech_sector_xlk.csv") -> pd.DataFrame:
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..",
                                                "data",
                                                file_name
                                                ))
        df = pd.read_csv(file_path)
        return df

        
    def fetch_and_transform_holdings_data(self) -> pd.DataFrame:
        """
        Note for PLTR, there is only data from 2020 onwards, so it will not be
        included
        """
        df_mapping = {}
        for holding in self.TOP_HOLDINGS_XLK:
            temp_df = self.fetch_full_historical_data(holding)
            temp_df = temp_df.set_index("date")
            DataPipeLine.get_log_returns(temp_df)
            temp_df = temp_df["log_returns"]
            print(f"Here is the transformed data for : {holding}\n {temp_df}")
            print()
            df_mapping[holding] = temp_df
        
        holdings_log_return_df = pd.concat(df_mapping, axis=1)
        return holdings_log_return_df
    
    def compute_rolling_correlation_matrices(self, holdings_log_returns_df: pd.DataFrame, window_size:int=30)-> List[Tuple[pd.Timestamp, np.ndarray]]:
        # for now using a window size of 30 since this showed the best "clustering"
        # in the log_returns of the XLK index as seen in the jupyter notebook
        df_values = holdings_log_returns_df.to_numpy()
        dates = holdings_log_returns_df.index
        args_list = [(df_values, dates, i, window_size) for i in range(len(holdings_log_returns_df) - window_size + 1)]

        with Pool() as pool:
            corr_matrices_with_dates = pool.map(DataPipeLine.compute_single_corr_matrix, args_list)

        return corr_matrices_with_dates

    @staticmethod
    def compute_single_corr_matrix(args: Tuple[pd.DataFrame, pd.Index, int, int])->Tuple[pd.Timestamp, np.ndarray]:
        df_values, dates, start, window_size = args
        window = df_values[start: start+window_size]
        corr_matrix = np.corrcoef(window, rowvar=False)
        window_end_date = dates[start+window_size-1]
        return window_end_date, corr_matrix
    
    def get_full_corr_matrices_of_holdings(self)->List[np.ndarray]:
        df = self.fetch_and_transform_holdings_data()
        return self.compute_rolling_correlation_matrices(df)

    @staticmethod
    def get_log_returns(df: pd.DataFrame)->None:
        #using the close prices for this
        df["log_returns"] = np.log(df["close"]/df["close"].shift(1))
        df.dropna(inplace=True)

    @staticmethod
    def get_intraday_price_range(df: pd.DataFrame)->None:
        df["price_range"] = abs(df["high"] - df["low"])

    @staticmethod
    def get_rolling_stats(df: pd.DataFrame, window_size:int=30) -> None:
        """
        This would be only for the actual XLK data

        Using 30-day since used the same for rolling corrs
        """
        if "log_returns" not in df.columns:
            DataPipeLine.get_log_returns(df)
        df[f"rolling_{window_size}_mean"] = df["log_returns"].rolling(window_size).mean()
        df[f"rolling_{window_size}_vol"] = df["log_returns"].rolling(window_size).std()
        df.dropna(inplace=True)

    @staticmethod
    def get_training_data(df: pd.DataFrame):
        DataPipeLine.get_intraday_price_range(df)
        DataPipeLine.get_log_returns(df)

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
        if old_df.empty:
            print("No Data in File Currently")
            df.to_csv(file_abs_path, index=False)
            return
        df = pd.concat([old_df, df], axis= 0, ignore_index=True)
        df.drop_duplicates(subset=["date"], inplace=True)
        df.sort_values(by="date", inplace=True)
        df.to_csv(file_abs_path, index=False)

    @staticmethod
    def change_data_format(file_name:str):
        # used for the data which I got online. This could be set as obsolete
        # but im just keeping this here in case I ever need it again
        file = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
        df = pd.read_csv(file)
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
        df.reset_index(drop=True, inplace=True)
        df.sort_values("date", inplace=True)
        df = df[DataPipeLine.COL_ORDER]
        df.to_csv(file, index=False)

if __name__ == "__main__":
    dp = DataPipeLine()
    file = os.path.join(os.path.dirname(__file__), '..', 'data', "tech_sector_xlk.csv")
    df = pd.read_csv(file)
    df.sort_values("date", inplace=True)
    df.to_csv(file, index=False)