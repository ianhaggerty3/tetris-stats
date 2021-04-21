import datetime
import glob
import os
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import pandas as pd
import numpy as np

REPLAY_GLOB = "G:/Applications/NullpoMino/replay/*.rep"
DATETIME_STR = "%Y_%m_%d_%H_%M_%S.rep"

if __name__ == '__main__':
    replay_files = list(map(lambda entry: os.path.basename(entry), glob.glob(REPLAY_GLOB)))
    replay_dates = sorted(list(map(lambda entry: datetime.datetime.strptime(entry, DATETIME_STR), replay_files)))
    print(f'got a list of length {len(replay_dates)}')

    date_count_dict = {}
    for date in replay_dates:
        key_str = date.strftime('%Y-%m')
        date_count_dict[key_str] = date_count_dict.get(key_str, 0) + 1

    count_list = []
    ticklabels = []
    for i in range(2020, last_date.year + 1):
        for j in range(1, 13):
            if i == 2020 and j < 5:
                continue
            if i == 2021 and j > 4:
                continue
            key_str = f'{i}-{j:02}'
            count_list.append(date_count_dict.get(key_str, 0))
            ticklabels.append(key_str)

    ax = plt.figure().add_subplot(111)
    ax.plot(count_list)

    ax.set_xticks(np.arange(0,len(ticklabels)))
    ax.set_xticklabels(ticklabels) #add monthlabels to the xaxis

    plt.xlabel('Date (Year-Month)')
    plt.ylabel('# of completed games')
    plt.title('Completed Tetris Games Per Month')

    # ax.legend(pt.columns.tolist(), loc='center left', bbox_to_anchor=(1, .5)) #add the column names as legend.
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    plt.show()
