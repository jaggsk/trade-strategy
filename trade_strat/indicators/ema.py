import pandas as pd

def exp_moving_average(ema_period = None,data_col= None):
    '''
    Function to create exponential moving average of a data series

    Arguments:
    ema_period (int): number of unit periods over which to calculate moving average
    data_col (float): pandas column input -  recommended to run on close
    sma_period = number of integer units to perform the rolling calculation. 
    
    Returns:
    Numpy array - declare as a new pandas column

    Raises:
    None

    Example:
    df['EMA'] = exp_moving_average(data_col=df.Close,sma_period=21)

    PRECONDITIONS: data column is longer than requested calculation period. Column slice is valid data.
    KJAGGS SEP 2022
    '''

    ema_col_numpy = data_col.to_numpy()
    ema_series = pd.Series(ema_col_numpy) 

    return ema_series.ewm(span=ema_period, min_periods=ema_period).mean().to_numpy()