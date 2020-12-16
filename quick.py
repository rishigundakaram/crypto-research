import pandas as pd 
from datetime import date, datetime
import stackprinter
import matplotlib.pyplot as plt
import numpy as np
stackprinter.set_excepthook(style='darkbg2')
from clean import file_chooser
from pprint import pprint


coins = ['BTC', 'DFN', 'DGX', 'EOS', 'ERC20', 'ETH', 'GNT', 'LTC', 'SC', 'STORJ', 'USDC', 'USDT', 'XTZ', 'ZEC']

def time_series(coins): 
    dic = {}
    for coin in coins: 
        fname = file_chooser(coin)
        coin_df = pd.read_csv(fname)
        dic[coin_df["snapped_at"][0]] = coin
    dates = [i for i in dic.keys()]
    dates.sort(reverse=False)
    for i in dates: 
        print(f"{dic[i]}: {i}")
    
time_series(coins)