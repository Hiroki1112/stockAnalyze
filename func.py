import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib

def trimmingData(df):
    #株価が-の時は前日終値を値として使う
    df.loc[df["株価"]=='-',"株価"] = df.loc[df["株価"]=='-',"前日終値"]


