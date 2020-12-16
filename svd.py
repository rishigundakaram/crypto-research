import numpy as np
import os
import stackprinter
from clean import normalizer_percent_change, normalizer_log, time_series, filter_time_series
from pprint import pprint
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
figure(figsize=(11,9))

stackprinter.set_excepthook(style='darkbg2')

dates_str =  {
    'total time': ['2017-05-01', '2020-11-25'],
    'pre-crash': ['2017-05-01', '2017-12-17'],
    'crash': ['2017-12-22', '2018-12-22'], 
    'post-crash': ['2018-12-22', '2020-11-25'],
}

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
    coins = os.listdir('./data')
    dates = ['total time', 'pre-crash', 'crash', 'post-crash']
    periods = ['week', 'month']
    data = time_series(coins)

    for period in periods:
        for date in dates:
            cur_data = filter_time_series(data, start_date=dates_str[date][0], end_date=dates_str[date][1], period=period, normalizer=normalizer_log)
            matrix, labels = time_series_matrix(cur_data)
            p, s, q = np.linalg.svd(matrix, full_matrices=False)
            energy = calculate_energy(s)
            plot_svd_2D(p, s, q, labels, round(energy[2], 3), period, date, 'log')
            # print(f"coins: {labels}\nnum coins: {len(labels)}\nenergy: {energy[2]}\nperiod: {period}\nrange: {date}")

def plot_svd_2D(p, s, q, labels, energy, period, timeframe, normalizer): 
    coim_trunc = q[:2,:]
    p_trunc = p[:,:2]
    approx = s[0] * np.outer(p_trunc[:,0], coim_trunc[0,:]) 
    approx = approx + s[1] * np.outer(p_trunc[:,1], coim_trunc[1,:]) 
    points = []
    for i in range(np.shape(approx)[0]): 
        point = np.linalg.pinv(coim_trunc.T) @ np.matrix(approx[i,:]).T
        point.flatten()
        point = [np.matrix.tolist(i)[0][0] for i in point]
        points.append(point)
    points = np.array(points)
    for i in range(len(labels)): 
        plt.scatter(points[i,0], points[i,1], label=labels[i])
    plt.legend()
    plt.title(f"energy: {energy}, period: {period}, timeframe: {timeframe}")
    plt.savefig(f"./plots/energy_{energy}_period_{period}_timeframe_{timeframe}_normalizaion_{normalizer}.png")
    plt.clf()


if __name__ == "__main__":
    singular_value_script()
    exit(1)


