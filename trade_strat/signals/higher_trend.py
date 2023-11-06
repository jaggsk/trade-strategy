import numpy as np
import pandas as pd

def higher_trend(input_col = None):
    '''
    Function to determine if the last datapoint in a sequence is higher then the second to last.
    Used to determine higher highs or higher lows in trading startegy

    Arguments:
    input_col (pandas col, float) - input pandas column

    Returns:
    Boolean - True is last value is higher than second to last value

    Raises:
    None

    Preconditions:
    Supplied pandas column is numeric with no inf values

    Example:
    test_boolean = higher_trend(input_col = df['Test'])
    '''

    x = input_col.to_numpy()
    x = x[~np.isnan(x)]
    return x[-1] > x[-2]