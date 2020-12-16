import numpy as np
import os
from clean import normalizer_percent_change, normalizer_log, time_series, filter_time_series
from pprint import pprint

def time_series_matrix(data): 
    labels = []
    # get max time range
    lengths = [len(data[i]) for i in data.keys()]
    cols = max(lengths)
    rows = len(data)
    matrix = np.zeros((rows, cols))
    for idx, coin in enumerate(data.keys()): 
        labels.append(coin)
        x = len(data[coin])
        points = list(data[coin]["price"])
        matrix[idx,:] = points
    return [matrix, labels]

def calculate_energy(singular): 
    total_energy = sum([i**2 for i in singular])
    levels = []
    for i in singular: 
        if not levels: 
            levels.append(0)
        else: 
            levels.append(levels[len(levels) - 1])
        levels[len(levels) - 1] += i**2
    levels = [i / total_energy for i in levels]
    return levels

def singular_value_script(): 
    coins = ['BTC', 'LTC', 'USDT', 'ETH', 'SC', 'ZEC', 'GNT', 'EOS', 'STORJ', 'ERC20', 'DGX', 'XTZ', 'USDC', 'DFN']
    for i in range(3, len(coins)): 
        data = time_series(coins[:i], period='month')
        matrix, temp = time_series_matrix(data, fill=False)
        _, s, _ = np.linalg.svd(matrix)
        energy = calculate_energy(s)
        assert(temp == coins[:i])
        if (energy[2] > .9): 
            print(f"success: {coins[:i]}\nsingular values: {s}\nenergy: {energy[2]}")
        else: 
            print(f"failure: energy: {energy[2]}")

def singular_value_script_2():
    coins = os.listdir('./data')
    dates = [
        ['2017-05-01', '2020-11-25'], 
        ['2017-05-01', '2017-12-17'], 
        ['2017-12-22', '2018-12-22'], 
        ['2018-12-22', '2020-11-25']
    ]
    periods = ['week', 'month']
    data = time_series(coins)

    for period in periods:
        for date in dates:
            cur_data = filter_time_series(data, start_date=date[0], end_date=date[1], period=period, normalizer=normalizer_log)
            matrix, labels = time_series_matrix(cur_data)
            _, s, _ = np.linalg.svd(matrix)
            energy = calculate_energy(s)
            print(f"coins: {labels}\nnum coins: {len(labels)}\nenergy: {energy[2]}\nperiod: {period}\nrange: {date}")

if __name__ == "__main__":
    singular_value_script_2()
    exit(1)


