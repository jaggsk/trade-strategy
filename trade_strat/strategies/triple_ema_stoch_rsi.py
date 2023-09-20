import pandas_ta as pta
import trade_strat as ts
import pandas as pd
import numpy as np

class triple_ema_stoch_rsi:

    '''
    Class to run a scan for trading signals on financial instruments.
    Scan generates stochatsic RSI, 3 X EMA and RSI Indicators
    Indicators are reviewed to determine EMA Gradient, Stoch RSI Crossover/Crossunder
    Long signal = all ema gradients are positive, stochastic rsi k crosses above stoch rsi d
    Short signal = all ema gradients are negative, stochastic rsi k crosses below stoch rsi d
    Additional flags added for stoch rsi & rsi > or < threshold values and close > or < fast ema

    Arguments:
    df_scan (pandas dataframe): input OHLC dataframe - contains Close as a minimum
    stoch_len (int): length of stochastic -  typically 14
    stochrsi_length (int): length of rsi within stochastic -  typically 14
    stoch_k (int): length of stochatsic k parameter -  typically 3
    stoch_d (int): length of stochatsic d parameter -  typically 3
    ema_slow_len (int): length of exponential moving average - suggested start point of 200
    ema_med_len (int): length of exponential moving average - suggested start point of 200
    ema_fast_len (int): length of exponential moving average - suggested start point of 200
    rsi_len (int): length of reference rsi within stochastic -  typically 14
    rsi_upper (int): threshold for rsi to be above or below - typically 50
    stoch_rsi_upper (float): threshold for overbought signal
    stoch_rsi_lower (int): threhsold for oversold signal
    
    Returns:
    Pandas dataframe - updated OHLC with the indicators generated from Arguments
    Signal column is a trade flag, 1 for long, -1 for short

    Raises:
    None

    Example:
    df_scan = weekly_stoch_rsi_scan(df_scan= df,stoch_len = 14,stochrsi_length=14,stoch_k = 3,stoch_d = 3,ema_slow_len = 200,ema_med_len = 50,ema_fast_len = 21, rsi_len = 14, stoch_rsi_upper = 80, stoch_rsi_lower = 20)
    

    PRECONDITIONS: Input dataframe contains 'Close' column and number of rows exceeds minimum required for calculationns either triple emas, stochastic rsi or rsi.
    KJAGGS SEP 2023
    '''

    def __init__(self,df_scan= None,stoch_len = None,stochrsi_length=None,stoch_k = None,stoch_d = None,ema_slow_len = None,ema_med_len = None,ema_fast_len = None, rsi_len = None, rsi_upper = 50, stoch_rsi_upper = None, stoch_rsi_lower = None):
        
        self.df = df_scan
        self.stoch_len = stoch_len
        self.stochrsi_length = stochrsi_length
        self.stoch_k = stoch_k
        self.stoch_d = stoch_d
        self.ema_slow_len = ema_slow_len
        self.ema_med_len = ema_med_len
        self.ema_fast_len = ema_fast_len
        self.rsi_len = rsi_len
        self.rsi_upper = rsi_upper
        self.stoch_rsi_upper = stoch_rsi_upper
        self.stoch_rsi_lower = stoch_rsi_lower
        
    def run_scan(self):
        
        self.df[['srsik','srsid']] = pta.stochrsi(close = self.df['Close'],length = self.stoch_len,rsi_length=self.stochrsi_length,k = self.stoch_k,d = self.stoch_d)
        self.df["EMA SLOW"] = ts.exp_moving_average(ema_period=self.ema_slow_len, data_col= self.df['Close'])
        self.df["EMA MED"] = ts.exp_moving_average(ema_period=self.ema_med_len, data_col= self.df['Close'])
        self.df["EMA FAST"] = ts.exp_moving_average(ema_period=self.ema_fast_len, data_col= self.df['Close'])

        self.df["RSI"] = pta.rsi(close =  self.df['Close'],length = self.rsi_len)

        self.df['EMA GRAD'] = ts.grad_check(grad_array=self.df[["EMA SLOW","EMA MED","EMA FAST"]])  
        
        self.df['Close > EMA'] = (self.df["Close"] > self.df["EMA FAST"]).astype(int)
        self.df['RSI threshold'] = ts.indicator_threshold(column = self.df['RSI'], upper_threshold = self.rsi_upper, lower_threshold = self.rsi_upper)
        self.df['Stoch RSI K threshold'] = ts.indicator_threshold(column = self.df['srsik'], upper_threshold = self.stoch_rsi_upper, lower_threshold = self.stoch_rsi_lower)
        self.df['Crossover'] = ts.crossover(self.df['srsik'],self.df['srsid'])
        
        self.df['Signal'] = 0
        conditions = [(self.df['EMA GRAD'] == 1) & (self.df['Crossover'] == 1), (self.df['EMA GRAD'] == -1)&  (self.df['Crossover'] == -1)]
        values = [1, -1]

        self.df['Signal'] = np.select(conditions, values, 0)

        return self.df