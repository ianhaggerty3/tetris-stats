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
    
    frame_counts = []
    for data_file in sorted(data_files):
        total_frames, lines_cleared, data = parse.get_file_info(data_file)
        frame_counts.append(total_frames)
    
    plt.plot(list(range(len(frame_counts))), list(map(lambda entry: (entry - 100) / 60, frame_counts)))
    plt.show()

    
