import threading 
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from typing import Dict, Any
from datetime import datetime
import warnings
import logging
import sys
import torch.nn as nn
import torch.optim as optim
from scipy.stats import norm

sys.path.append("..") # check parent for modules

from dataPipeline.fetchData import DataPipeLine

class HMMDetectionEngine:
    def __init__(self):
        self.history = {}
        self.regime_data: Dict[str, tuple] = {}
        self.regime_distributions: Dict[str, Any] = {}
        self.transition_matrix: np.ndarray = None
    
    def pca(self):
        """
        This could be used to get the latent drift and vol
        """
        pass

    def rolling_sector_correlation(self, sector: str):
        """
        Based on the sector, compute the rolling correlation
        between stocks in that sector.
        This endogenous features adds detail to HMM model.
        """
        pass

    def calibrate(self):
        pass

    def gaussian_likelihood(self):
        pass

    def display_transition_matrix(self):
        pass

    def display_regime_distributions(self):
        pass

    def get_regime(self):
        """
            uses gaussian likelihoods to determine most probable
        """
        pass

