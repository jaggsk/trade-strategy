import pandas as pd
import numpy as np

def simple_moving_average(sma_period = None,data_col= None):
    '''
    Function to create simplemoving average of a data series

    Arguments:
    sma_period (int): number of unit periods over which to calculate moving average
    data_col (float): pandas column input -  recommended to run on close
    sma_period = number of integer units to perform the rolling calculation. 
    
    Returns:
    Numpy array - declare as a new pandas column

    Raises:
    None

    Example:
    df['SMA'] = simple_moving_average(data_col=df.Close,sma_period=21)

    PRECONDITIONS: data column is longer than requested calculation period. Column slice is valid data.
    KJAGGS SEP 2022
    '''

    ma_col_numpy = data_col.to_numpy()
    ma_series = pd.Series(ma_col_numpy) 

    return ma_series.rolling(sma_period).mean().to_numpy()
