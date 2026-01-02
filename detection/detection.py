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
from hmmlearn.hmm import GaussianHMM
from scipy.stats import norm
import json

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

    def train_hmm(self):
        pass

    def save_model_to_json(self, file_name: str):
        """
        This is mainly used to be able to export this somewher else
        and potentially use it in some other language in the future.
        """
        pass

