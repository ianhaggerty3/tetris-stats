import datetime
import glob
import os
import sys
import sys

from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import numpy as np

sys.path.append(os.path.abspath('../tetris_stats'))
import parse

REPLAY_GLOB = "G:/Applications/NullpoMino/replay/*.rep"
DATETIME_STR = "%Y_%m_%d_%H_%M_%S.rep"

if __name__ == '__main__':
    replay_files = glob.glob(REPLAY_GLOB)
    replay_dates = sorted(list(map(lambda entry: datetime.datetime.strptime(os.path.basename(entry), DATETIME_STR), replay_files)))

    date_count_dict = {}
    pps_dict = {}

    for replay_file, date in zip(replay_files, replay_dates):
        key_str = date.strftime('%Y-%m')
        game_info = parse.get_file_info(replay_file, frames=False)
        
        # only consider sprint games which are finished
        # should range from 40 to 43 lines; checking upper bound eliminates 
        # most marathon replays
        if game_info.lines >= 40 and game_info.lines < 44:
            date_count_dict[key_str] = date_count_dict.get(key_str, 0) + 1
            pps_dict[key_str] = pps_dict.get(key_str, []) + [game_info.pps]

    count_list = []
    pps_avg_list = [] # average the top 25% of pps results
    ticklabels = []

    # filter the data to the zone without any gaps
    last_date = replay_dates[-1]
    for i in range(2020, last_date.year + 1):
        for j in range(1, 13):
            if i == 2020 and j < 5:
                continue
            if i == 2021 and j > 4:
                continue
            key_str = f'{i}-{j:02}'
            count_list.append(date_count_dict.get(key_str, 0))
            pps_list = pps_dict.get(key_str, [])
            top_pps_list = pps_list[(3 * len(pps_list)) // 4:]
            avg = sum(top_pps_list) / len(top_pps_list) if len(top_pps_list) != 0 else 0
            pps_avg_list.append(avg)
            ticklabels.append(key_str)

    # pps histogram month to consider
    month_of_interest = 2
    year_of_interest = 2021
    hist_key = f'{year_of_interest}-{month_of_interest:02}'

    ax = plt.figure().add_subplot(111)
    ax.bar(list(range(len(count_list))), count_list)

    ax.set_xticks(np.arange(0,len(ticklabels)))
    ax.set_xticklabels(ticklabels) #add monthlabels to the xaxis

    plt.xlabel('Date (Year-Month)')
    plt.ylabel('Number of Completed Games')
    plt.title('Completed Tetris Games Per Month')

    plt.tight_layout(rect=[0, 0, 0.85, 1])

    plt.show()

    ax = plt.figure().add_subplot(111)
    ax.scatter(list(range(len(pps_avg_list))), pps_avg_list)

    ax.set_xticks(np.arange(0,len(ticklabels)))
    ax.set_xticklabels(ticklabels) #add monthlabels to the xaxis

    plt.xlabel('Date (Year-Month)')
    plt.ylabel('Average PPS (Pieces Per Second)')
    plt.title('Average PPS Over Time')

    plt.tight_layout(rect=[0, 0, 0.85, 1])

    plt.show()

    ax = plt.figure().add_subplot(111)
    ax.hist(pps_dict[hist_key], bins=20)

    plt.xlabel('PPS (Pieces Per Second)')
    plt.ylabel('Number of Completed Games')
    plt.title('PPS Histogram for February 2021')

    plt.show()
