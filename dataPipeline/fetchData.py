from turtle import st
import pandas as pd
import numpy as np
import websockets
import threading
import asyncio
import requests
from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.live import StockDataStream, OptionDataStream
from dotenv import load_dotenv
import os

load_dotenv()
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET_KEY = os.getenv("ALPACA_API_SECRET_KEY")

class DataPipeLine:
    def __init__(self):
        self.client = None
        self.stream = None
        self.connect_to_alpaca()

    def connect_to_alpaca(self):
        try:
            pass
        except Exception as e:
            print(f"Error connecting to Alpace: {e}")

    def fetch_historical_data(self):
        try:
            pass
        except Exception as e:
            print(f"Error fetching historical data: {e}")

    def fetch_live_data(self):
        try:
            pass
        except Exception as e:
            print(f"Error fetching live data: {e}")

    def display_data_in_terminal(self):
        pass

    def get_training_data(self):
        pass 

    @staticmethod
    def save_data_to_csv(df: pd.DataFrame, file_name:str):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
        df.to_csv(file_path, index=False)

    @staticmethod
    def save_data_to_existing_csv(df: pd.DataFrame, file_name:str):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
        old_df = pd.read_csv(file_name)
        df = pd.concat([old_df, df], axis= 0, ignore_index=True)
        df.sort_values(by="date", inplace=True)
        df.to_csv(file_path, index=False)
    
