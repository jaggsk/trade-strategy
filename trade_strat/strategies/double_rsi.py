import numpy as np
import pandas as pd
import trade_strat as ts
import pandas_ta as pta
import math
from scipy.signal import argrelextrema

class double_rsi:

    '''
    Class to run a scan for trading signals on financial instruments.
    Scan generates a fast RSI (default length = 2) and slow RSI (default length = 14)
    Indicators are reviewed to determine the following:
    Fast RSI crossing above and below a predetermined high low threshold
    local high/low on fast period rsi (above and below threshold only). Eqv values at these points are extraced from RSI Slow
    Long signal = RSI Fast crossing up above low threshold - higher low observed on RSI Slow between last 2 RSI Fast local minima
    Short signal = RSI Fast crossing up above low threshold - lower high observed on RSI Slow between last 2 RSI Fast local maxima
    Additional flags added for 

    Arguments:
    df_scan (pandas dataframe): input OHLC dataframe - contains Opn, High, Low, Close as a minimum
    fast_rsi_len (int): length of fast rsi -  default = 2
    slow_rsi_len (int): length of slow rsi -  default = 14
    rsi_threshold_low (float): value of low value crossover for long signal -  default = 15.0
    rsi_threshold_high (float): value of high value crossunder for short signal -  default = 85.0
    local_hl_period(int): scanning period for argrelextrema, used to detect local highs/lows default = 5

    Returns:
    Pandas dataframe - updated OHLC with the indicators generated from Arguments
    Signal column is a trade flag, 1 for long, -1 for short

    Raises:
    None

    Example:
    df = double_rsi(df_scan = df,fast_rsi_len= 2,slow_rsi_len= 14,rsi_threshold_low=15.0,rsi_threshold_high = 85.0,local_hl_period=5)
    

    PRECONDITIONS: Input dataframe contains 'Close' column and number of rows exceeds minimum required for calculationns either triple emas, stochastic rsi or rsi.
    KJAGGS OCT 2023
    '''

    def __init__(self,df_scan = None,fast_rsi_len= 2,slow_rsi_len= 14,rsi_threshold_low=15.0,rsi_threshold_high = 85.0,local_hl_period=5):
        
        self.df_scan = df_scan
        self.fast_rsi_len = fast_rsi_len
        self.slow_rsi_len = slow_rsi_len
        self.rsi_threshold_low = rsi_threshold_low
        self.rsi_threshold_high = rsi_threshold_high
        self.local_hl_period = local_hl_period

    def run_scan(self):
         
        #create indicators 
        self.df_scan['RSI Slow'] = pta.rsi(close =  self.df_scan['Close'],length = self.slow_rsi_len)
        self.df_scan['RSI Fast'] = pta.rsi(close =  self.df_scan['Close'],length = self.fast_rsi_len)

        #determine if RSI is above/below or crossing thresholds
        self.df_scan['RSI Threshold'] = ts.indicator_threshold(column = self.df_scan['RSI Fast'], upper_threshold = self.rsi_threshold_low, lower_threshold = self.rsi_threshold_high)
        self.df_scan['RSI Low Limit'] = self.df_scan['RSI Fast'].shift(1) < self.rsi_threshold_low
        self.df_scan['RSI High Limit'] = self.df_scan['RSI Fast'].shift(1) > self.rsi_threshold_high

        #genrate signals
        self.df_scan['RSI Fast Signal'] = ts.crossover_fixed(lead_col = self.df_scan['RSI Fast'], threshold_low = self.rsi_threshold_low, threshold_high = self.rsi_threshold_high)
        
        self.df_scan['Local Max'] = self.df_scan.iloc[argrelextrema(self.df_scan['RSI Fast'].values, np.greater, order=self.local_hl_period)[0]]['RSI Fast']
        self.df_scan['Local Min'] = self.df_scan.iloc[argrelextrema(self.df_scan['RSI Fast'].values, np.less, order=self.local_hl_period)[0]]['RSI Fast']

        self.df_scan['Local Max'] = np.where((self.df_scan['Local Max'] < self.rsi_threshold_high) & (self.df_scan['Local Max'].notna()) ,np.NaN,self.df_scan['Local Max'])
        self.df_scan['Local Min'] = np.where((self.df_scan['Local Min'] > self.rsi_threshold_low) & (self.df_scan['Local Min'].notna()) ,np.NaN,self.df_scan['Local Min'])

        #extract RSI slow values where the RSI Fast shows a crossover
        self.df_scan['RSI Trend Min'] = np.where((self.df_scan['Local Min'].isna()) ,np.NaN,self.df_scan['RSI Slow'])
        self.df_scan['RSI Trend Max'] = np.where((self.df_scan['Local Max'].isna()) ,np.NaN,self.df_scan['RSI Slow'])

        #determine if higher low or higher high is true
        self.df_scan['Higher High'] = False
        self.df_scan['Higher Low'] = False

        #iterative placeholders
        rsi_low_ref = False
        rsi_high_ref = False
        rsi_high_first = None
        rsi_high_second = None
        higher_high = False
        higher_low = False

        for i, row in self.df_scan.iterrows():

            if math.isnan(self.df_scan.at[i,'RSI Trend Max']) == False:
                if rsi_high_ref == False:
                  rsi_high_second = self.df_scan.at[i,'RSI Trend Max']
                  rsi_high_ref = True
                else:
                  rsi_high_first = rsi_high_second
                  rsi_high_second = self.df_scan.at[i,'RSI Trend Max']
                  higher_high = rsi_high_first < rsi_high_second

            if math.isnan(self.df_scan.at[i,'RSI Trend Min']) == False:
                if rsi_low_ref == False:
                  rsi_low_second = self.df_scan.at[i,'RSI Trend Min']
                  rsi_low_ref = True
                else:
                  rsi_low_first = rsi_low_second
                  rsi_low_second = self.df_scan.at[i,'RSI Trend Min']
                  higher_low = rsi_low_first < rsi_low_second
            
            #update dataframe with current high/low status
            self.df_scan.at[i,'Higher Low'] = higher_low            
            self.df_scan.at[i,'Higher High'] = higher_high

        #signal conditions
        self.df_scan['Signal'] = 0
        conditions = [(self.df_scan['RSI Fast Signal'] == 1) & (self.df_scan['Higher Low'] == True), (self.df_scan['RSI Fast Signal'] == -1)&  (self.df_scan['Higher High'] == False)]
        values = [1, -1]

        self.df_scan['Signal'] = np.select(conditions, values, 0)
        
        return self.df_scan