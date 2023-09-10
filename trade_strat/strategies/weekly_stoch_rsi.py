import pandas_ta as pta
import trade_strat.indicators as id

class weekly_stoch_rsi:

    '''
    Class to run a weekly scan on yahoo finance domain instruments.
    Scan generates stochatsic RSI, EMA and RSI Indicators
    Indicators are reviewed to determine EMA Gradient, Stoch RSI Crossover/Crossunder

    Arguments:
    df_scan (pandas dataframe): input OHLC dataframe - contains Close as a minimum
    stoch_len (int): length of stochastic -  typically 14
    stochrsi_length (int): length of rsi within stochastic -  typically 14
    stoch_k (int): length of stochatsic k parameter -  typically 3
    stoch_d (int): length of stochatsic d parameter -  typically 3
    ema_len (int): length of exponential moving average - suggested start point of 21
    rsi_len (int): length of reference rsi within stochastic -  typically 14
    stoch_rsi_upper (float): threshold for overbought signal
    stoch_rsi_lower (int): threhsold for oversold signal
    
    Returns:
    Pandas dataframe - updated OHLC with the indicators generated from Arguments

    Raises:
    None

    Example:
    df_scan = weekly_stoch_rsi_scan(df_scan= df,stoch_len = 14,stochrsi_length=14,stoch_k = 3,stoch_d = 3,ema_len = 21, rsi_len = 14, stoch_rsi_upper = 80, stoch_rsi_lower = 20)
    

    PRECONDITIONS: Input dataframe contain 'Close' column and number of rows exceeds minimum required for calculationns either ema, stochastic rsi or rsi.
    KJAGGS SEP 2023
    '''

    def __init__(self,df_scan= None,stoch_len = None,stochrsi_length=None,stoch_k = None,stoch_d = None,ema_len = None, rsi_len = None, stoch_rsi_upper = None, stoch_rsi_lower = None):
        
        self.df = df_scan
        self.stoch_len = stoch_len
        self.stochrsi_length = stochrsi_length
        self.stoch_k = stoch_k
        self.stoch_d = stoch_d
        self.ema_len = ema_len
        self.rsi_len = rsi_len
        self.stoch_rsi_upper = stoch_rsi_upper
        self.stoch_rsi_lower = stoch_rsi_lower
        
    def run_scan(self):
        
        self.df[['srsik','srsid']] = pta.stochrsi(close = self.df['Close'],length = self.stoch_len,rsi_length=self.stoch_k,k = 3,d = self.stoch_d)
        self.df["EMA"] = pta.ema(close = self.df.Close,length = self.ema_len)
        self.df["RSI"] = pta.rsi(close =  self.df['Close'],length = self.rsi_len)

        self.df["EMA GRAD"] = self.df["EMA"].diff()        
        self.df['Close > EMA'] = (self.df["Close"] > self.df["EMA"]).astype(int)
        self.df['Stoch RSI K threshold'] = id.indicator_threshold(column = self.df['srsik'], upper_threshold = self.stoch_rsi_upper, lower_threshold = self.stoch_rsi_lower)
        self.df['Crossover'] = id.crossover(self.df['srsik'],self.df['srsid'])
        
        return self.df