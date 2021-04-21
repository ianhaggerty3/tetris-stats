from __future__ import annotations

import datetime
import math
import os
import re
import sys

from typing import Iterable, Tuple, Union

# REPLAY FILE FORMAT (NullpoMino)
# replay files contain information about which buttons are pressed on which frame.
# a line is added to the file on each frame a key is either pressed down or released.
# each button is mapped to a power of two. If two keys are pressed at the same time,
# those powers of two are simply added together.
# Frame-specific key information is stored in the following form:
#   `0.r.{frame_num}={key_sum}`

REPLAY_FILE_EXTENSION = '.rep'
DATETIME_STR = "%Y_%m_%d_%H_%M_%S.rep"

# a mapping of the powers of two to key actions
button_dict = {
    '0': 'none',
    '1': 'hard drop',
    '2': 'soft drop',
    '4': 'left',
    '8': 'right',
    '16': 'ccw',
    '32': 'cw',
    '128': 'hold',
    '256': 'flip',
}

action_dict = {v: k for k, v in button_dict.items()}

frame_info_pattern = f'^0.r.(?P<frame_num>[1-9][0-9]*)=(?P<key_sum>0|[1-9][0-9]*)$'
max_frame_pattern = f'^0.r.max=(?P<max_frame>[1-9][0-9]*)$'
num_lines_pattern = f'^0.statistics.lines=(?P<num_lines>0|[1-9][0-9]*)$'
num_pieces_pattern = f'^0.statistics.totalPieceLocked=(?P<num_pieces>0|[1-9][0-9]*)$'
pps_pattern = f'^0.statistics.pps=(?P<pps>[0-9]\.[0-9]*)$'


class GameInfo():
    def __init__(self, name: str, lines: int, pieces: int, frames: int, \
                 pps: float, data: Iterable[Tuple[int, int]]):
        self.name = name     # file name (contains date info)
        self.date = datetime.datetime.strptime(os.path.basename(name), DATETIME_STR)
        self.lines = lines   # total lines cleared in a game
        self.pieces = pieces # total pieces dropped in a game
        self.frames = frames # total frames in a game
        self.pps = pps       # pieces per second
        self.data = list(data)

def button_held(key_sum: int, action: str):
    if action not in action_dict:
        raise KeyError('checking for invalid action')
    key = int(action_dict[action])
    if key & key_sum != 0:
        return True
    return False

def get_line_attrs(line: str) -> Union[None, Tuple[int, int]]:
    match = re.search(frame_info_pattern, line)
    if match is None:
        return None
    frame_num = int(match.group('frame_num'))
    key_sum = int(match.group('key_sum'))
    return frame_num, key_sum

def get_total_frames(lines: Iterable[str]) -> int:
    for line in lines:
        match = re.match(max_frame_pattern, line)
        if match is not None:
            return int(match.group('max_frame'))
    
    raise ValueError("File doesn't log final frame")

def get_total_pieces(lines: Iterable[str]) -> int:
    for line in lines:
        match = re.match(num_pieces_pattern, line)
        if match is not None:
            return int(match.group('num_pieces'))
    
    raise ValueError("File doesn't log total pieces dropped")

def get_pps(lines: Iterable[str]) -> float:
    for line in lines:
        match = re.match(pps_pattern, line)
        if match is not None:
            return float(match.group('pps'))
    
    raise ValueError("File doesn't log pps")

def get_lines_cleared(lines: Iterable[str]) -> int:
    for line in lines:
        match = re.match(num_lines_pattern, line)
        if match is not None:
            return int(match.group('num_lines'))
    
    raise ValueError("File doesn't log total lines cleared")

def get_file_info(filename: str) -> GameInfo:
    with open(filename, 'r') as fid:
        data = sorted(filter(None, map(get_line_attrs, fid)))
        
        fid.seek(0)
        try:
            total_frames = get_total_frames(fid)
        except ValueError:
            raise ValueError(f"{filename} doesn't log final frame")
        
        fid.seek(0)
        try:
            total_pieces = get_total_pieces(fid)
        except ValueError:
            raise ValueError(f"{filename} doesn't log total pieces dropped")

        fid.seek(0)
        try:
            lines_cleared = get_lines_cleared(fid)
        except ValueError:
            raise ValueError(f"{filename} doesn't log total lines cleared")
        
        fid.seek(0)
        try:
            pps = get_pps(fid)
        except ValueError:
            raise ValueError(f"{filename} doesn't log pps")

    return GameInfo(filename, lines_cleared, total_pieces, total_frames, pps, data)

# example usage
if __name__ == '__main__':
    data_file = input('please input the path to a test replay file: \n>>> ')
    if not os.path.exists(data_file) or not data_file.endswith('.rep'):
        print('invalid data file')
        sys.exit(1)
    
    game_info = get_file_info(data_file)
    print(list(game_info.data))
