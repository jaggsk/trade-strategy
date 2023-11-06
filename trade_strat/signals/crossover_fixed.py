import numpy as np
import pandas as pd

def crossover_fixed(lead_col = None, threshold_low = None, threshold_high = None):
    
    '''
    Function to determine when a signal cross above a lower bound and below a higher bound.

    Arguments:
    lead col (pandas col, float) - pandas column for lead signal
    threshold_low (float) - fixed reference value, signal crosses above value from below
    threshold_high (float(- fixed reference value, signal crosses below value from above

    Returns:
    Numpy array - declare as a new pandas column
    Where lead column crosses above low threshold from below = -1
    Where lead column crosses down from above high threshold = 1 

    Raises:
    None

    Preconditions:
    Supplied pandas column is numeric with no Nan, inf values
    Supplied thresholds are floats and signal column will intersect value range

    Example:
    df['crossover'] = self.df['RSI'], threshold_low = 20, threshold_high = 80)
    '''

    #convert input to numpy arrays
    lead_col_numpy = lead_col.to_numpy()

    #define arrays
    array_crossover_low = np.zeros(lead_col.shape[0], dtype=int)
    array_crossover_high = np.zeros(lead_col.shape[0], dtype=int)
    array_threshold_low = np.zeros(lead_col.shape[0], dtype=int)
    array_threshold_high = np.zeros(lead_col.shape[0], dtype=int)
    
    #fill threshold values with constant
    array_threshold_low.fill(threshold_low)
    array_threshold_high.fill(threshold_high)

    #calculate crossovers signal -1 for low crossover +1 for high crossunder
    #remove unwanted values from crossover and crossunder
    array_crossover_low[1:lead_col.shape[0]] = np.diff((lead_col_numpy >array_threshold_low).astype(int))
    array_crossover_low[array_crossover_low == -1] = 0
    array_crossover_high[1:lead_col.shape[0]] = np.diff((lead_col_numpy < array_threshold_high).astype(int)*-1) 
    array_crossover_high[array_crossover_high == 1] = 0
    
    #return sum of arrays -1 = short +1 = long
    return array_crossover_low + array_crossover_high
