# TODO: Fix these strange imports

import sys
import os
sys.path.append(os.path.abspath('../tetris_stats'))

import parse
from matplotlib import pyplot as plt
import glob


if __name__ == '__main__':
    data_files = glob.glob('../../tests/best_replays/*')
    print(data_files)
    
    pps = []
    for data_file in sorted(data_files):
        game_info = parse.get_file_info(data_file)
        pps.append(game_info.pps)
    
    plt.plot(list(range(len(frame_counts))), pps)
    plt.show()
