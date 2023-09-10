import numpy as np

def crossover(lead_col = None, trailing_col = None):
    
    '''
    Function to determine where two signals cross each other.

    Arguments:
    lead col - pandas column for lead signal
    trailing col - pandas column for trailing signal

    Returns:
    Numpy array - declare as a new pandas column
    Where lead column crosses above trailing column = 1
    Where trailing column crosses above lead column = -1 

    Raises:
    None

    Preconditions:
    Supplied pandas columns are numeric and same length

    Example:
    df['crossover'] = crossover(df['column one'],df['column two'])
    '''

    #convert to mupy arrays
    lead_col_numpy = lead_col.to_numpy()
    trailing_col_numpy = trailing_col.to_numpy()

    array_crossover = np.zeros(lead_col.shape[0], dtype=int)
    array_crossover[1:lead_col.shape[0]] = np.diff((lead_col_numpy >trailing_col_numpy).astype(int)) 
    
    return array_crossover  