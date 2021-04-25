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
import analyze

FIRST_GAME_FRAME = 100
FRAMES_PER_SECOND = 60

if __name__ == '__main__':
    game_of_interest = '../../tests/best_replays/2021_02_11_15_51_52.rep'
    game_info = parse.get_file_info(game_of_interest, frames=True)

    drops = list(filter(
        lambda entry: entry is not None and game_info.data[entry][0] >= FIRST_GAME_FRAME,
        map(analyze.get_drops(), enumerate(game_info.data))))
    
    # print(f'len(piece_changes) = {len(drops)} game_info.pieces = {game_info.pieces}')

    discrete_pps_list = [None] * len(drops)
    discrete_pps_frames = [None] * len(drops)
    for i, drop in enumerate(drops):
        frame = game_info.data[drop][0]
        local_pps = ((i + 1) / (frame - FIRST_GAME_FRAME)) * FRAMES_PER_SECOND
        # print(f'local_pps = {local_pps}')
        discrete_pps_list[i] = local_pps
        discrete_pps_frames[i] = frame

    ax = plt.figure().add_subplot(111)
    ax.plot(discrete_pps_frames, discrete_pps_list)

    plt.xlabel('Frame Number')
    plt.ylabel('Local PPS (Pieces Per Second)')
    plt.title('PPS Throughout My Personal Best')

    plt.ylim((2, 4))

    plt.tight_layout(rect=[0, 0, 0.85, 1])

    plt.show()
