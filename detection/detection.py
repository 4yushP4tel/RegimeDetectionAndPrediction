import threading 
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime
import warnings
import logging
import sys
from hmmlearn import hmm

sys.path.append("..") # check parent for modules

from dataPipeline.fetchData import DataPipeLine

class HMMDetectionEngine:
    def __init__(self):
        self.history = {}

    def calibreate():
        pass

    def gaussian_likelihood():
        pass

    def get_regime():
        """
        Determine the current vol regime based on transition matrix and
        past data
        """
        pass

