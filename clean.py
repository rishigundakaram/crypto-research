import pandas as pd 
from datetime import date, datetime
import stackprinter
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
from math import log, log10
# stackprinter.set_excepthook(style='darkbg2')

default_start_date_str = '2010-1-1'
default_start_date = datetime.strptime(default_start_date_str, '%Y-%m-%d')
def file_chooser(coin): 
    return f'./data/{coin.upper()}/{coin.lower()}-usd-max.csv'


def normalizer_log(col): 
    changes = []
    for i in col: 
        if not changes: 
            changes.append(0)
        else: 
            changes.append(log10(i / prev))
        prev = i
    return changes

def normalizer_percent_change(col): 
    changes = []
    for i in col: 
        if not changes: 
            changes.append(0)
        else: 
            changes.append(((i / prev) - 1) * 100)
        prev = i
    return changes
    
def time_series(coins): 
    data = {}
    for coin in coins: 
        fname = file_chooser(coin)
        coin_df = pd.read_csv(fname)
        coin_df = coin_df.rename(columns={"snapped_at":"date"})
        coin_df["date"] = pd.to_datetime(coin_df["date"])
        data[coin] = coin_df
    return data


def filter_time_series(data, start_date=default_start_date_str, end_date=date.today(), period='week', normalizer=normalizer_percent_change): 
    coins = {}
    for i in data: 
        # filter by period first
        coins[i] = data[i].copy(deep=True)
        df = coins[i]
        if period == 'week': 
            day_num = datetime.strptime(start_date, '%Y-%m-%d').weekday()
            df = df.loc[df["date"].dt.weekday == day_num]
        elif period == 'month': 
            df = df.loc[df["date"].dt.is_month_start]
        df = df.set_index(["date"])
        # filter by date next
        df = df.loc[start_date:end_date]
        # normalize data
        df["price"] = normalizer(df["price"])
        coins[i] = df
    choose = max([len(coins[i]) for i in coins.keys()])
    new_coins = []
    for i in data.keys(): 
        if len(coins[i]) != choose: 
            new_coins.append(i)
    for i in new_coins: 
        del coins[i]
    return coins

def plot_time_series(data): 
    labels = []
    for coin in data.keys():
        plt.plot(data[coin].index.tolist(), data[coin]["price"])
        labels.append(coin)
    plt.legend([i.upper() for i in labels])
    plt.ylabel("%change")
    plt.xlabel("year")
    plt.title("%change vs time")
    plt.show() 

if __name__ == "__main__":
    coins = ['ERC20', 'DGX', ]
    data = time_series(coins, period='month', start_date='2017-01-01' ,end_date='2019-10-10', normalizer=normalizer_percent_change)
    plot_time_series(data)


