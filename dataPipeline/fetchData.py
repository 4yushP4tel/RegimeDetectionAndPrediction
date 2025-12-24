import pandas as pd
import numpy as np
import websockets
import threading
import asyncio
import requests
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.live import StockDataStream
from dotenv import load_dotenv
import os

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
        pass

    def fetch_live_data(self):
        pass

    def process_data(self):
        pass

    def display_data_in_terminal(self):
        pass