''' Code template from QSTK tutorial used.'''

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np
import math
import itertools

def simulate(dt_start, dt_end, ls_symbols, alloc):

    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    d_data = d_data['actual_close']
    d_data = d_data.fillna(method='ffill')
    d_data = d_data.fillna(method='bfill')
    temp_data = d_data.values
    normalized = temp_data/temp_data[0, :]
    for allocIndex in range(len(ls_symbols)):
        normalized[:, allocIndex] = normalized[:, allocIndex]*alloc[allocIndex]
    cumulative_return = normalized.sum(axis = 1)
    returns = [0]
    for i in range(1, len(cumulative_return)):
        returns.append(cumulative_return[i]/cumulative_return[i-1] - 1)
    daily_return = np.mean(returns)
    std_dev = np.std(returns)
    sharpe = 1.0*math.sqrt(252)*daily_return/std_dev
    final_cumulative_return = cumulative_return[-1]
    return std_dev, daily_return ,sharpe, final_cumulative_return


def main():
    
    ls_symbols = [sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10]]
    dt_start = dt.datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    dt_end = dt.datetime(int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
        
    alloc = [0.0, 0.0, 0.0, 0.0]
    max_sharpe, final_std_dev, final_daily_return, final_cumulative_return = 0,0,0,0
    best_alloc = alloc

    possiblePermutations = list(itertools.permutations([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]*4, 4))
    print("All permutations done")
    validPermutaions = [] # sum to one
    for perm in possiblePermutations:
        if sum(perm) != 1:
            continue
        else:
        if(not perm in validPermutaions):  # unique permutations
                validPermutaions.append(perm)
    print("Valid Permtations Acquired")
    for each in validPermutaions:
        std_dev, daily_return, sharpe, cumulative_return = simulate(dt_start, dt_end, ls_symbols, each)
        if sharpe > max_sharpe:
            max_sharpe = sharpe
            final_std_dev = std_dev
            final_cumulative_return = cumulative_return
            final_daily_return = daily_return
            best_alloc = each

    print "Symbols: ", ls_symbols
    print "Best Portfolio: ", best_alloc
    print "Volatility: ", final_std_dev
    print "Daily Returns: ", final_daily_return
    print "Cumulative Returns: ", final_cumulative_return
    print "Sharpe Ratio: ", max_sharpe


if __name__ == '__main__':
    main()