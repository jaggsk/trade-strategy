def indicator_threshold(column = None, upper_threshold = None, lower_threshold = None):
    '''
    Function to determine where a signal is above or below predefined thresholds.

    Arguments:
    column (pandas)- pandas column for input signal
    upper threshold (float/int) - limit above which a signal is returned
    lower threshold (float/int) - limit below which a signal is returned
    
    Returns:
    Numpy array - declare as a new pandas column
    Where signal > upper_threshold = 1
    Where signal < lower_threshold = -1

    Raises:
    None

    Preconditions:
    Supplied pandas columns are numeric and same length

    Example:
    df['threshold'] = indicator_threshold(column = df['signal'], upper_threshold = 80, lower_threshold = 20)
    '''
    array_upper = (column.to_numpy() > upper_threshold).astype(int)
    array_lower = (column.to_numpy() < lower_threshold).astype(int) *-1

    return array_upper + array_lower

