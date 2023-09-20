import pandas as pd
import numpy as np

def grad_check(grad_array=None):

    '''
    Function to determine if time series gradients for any number of signals are positive or negative.
    Delta Y is considered 1 in all cases.
    (X2-X1)/1

    Arguments:
    grad_array (float): selecte dcolumnds from input pandas dataframe

    Returns:
    Numpy array - declare as a new pandas column
    1 = All gradients are positive
    -1 = All gradients are negative

    Raises:
    AttributeError if grad_array is not declared and defaults to None.

    Example:
    df['Grad Check'] = grad_check(df[['EMA Slow','EMA Mid','EMA Fast']])

    PRECONDITIONS: data columns are idenitcal dimensions. Column slice is valid data input data.
    KJAGGS SEP 2023
    '''

    try:
        grad_array_numpy = grad_array.diff().to_numpy()
        
    except AttributeError as err:
        print("grad_array is None")
        return None

    all_pos = np.zeros(grad_array.shape[0], dtype=int)
    all_pos = np.where(np.all(np.sign(grad_array_numpy) >= 0, axis = 1),1,0)
    all_neg = np.zeros(grad_array.shape[0], dtype=int)
    all_neg = np.where(np.all(np.sign(grad_array_numpy) < 0, axis = 1),-1,0)

    return all_pos+all_neg 

