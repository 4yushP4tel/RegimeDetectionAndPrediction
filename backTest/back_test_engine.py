import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import sys

sys.append("..")

from detection.detection import HMMDetectionEngine

class BackTestEngine:
    def __init__(self):
        self.results: pd.DataFrame = None

    def compute_sharpe_ratio(self):
        pass

    def run_backtest(self):
        pass

    

    