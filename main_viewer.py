import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from datetime import datetime
from detection.detection import HMMDetectionEngine
import sys

class Viewer:
    def __init__(self):
        pass

    @staticmethod
    def start():
        st.title("Regime Detection Viewer")


if __name__ == "__main__":
    Viewer.start()