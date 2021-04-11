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
num_lines_pattern = f'^0.statistics.lines=(?P<num_lines>0|[1-9][0-9]*)'


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

def get_lines_cleared(lines: Iterable[str]) -> int:
    for line in lines:
        match = re.match(num_lines_pattern, line)
        if match is not None:
            return int(match.group('num_lines'))
    
    raise ValueError("File doesn't log total lines cleared")

def get_file_info(filename: str) -> Tuple[int, int, Iterable[Tuple[int, int]]]:
    with open(filename, 'r') as fid:
        data = sorted(filter(None, map(get_line_attrs, fid)))
        fid.seek(0)
        try:
            total_frames = get_total_frames(fid)
        except ValueError:
            raise ValueError(f"{filename} doesn't log final frame")
        fid.seek(0)
        try:
            lines_cleared = get_lines_cleared(fid)
        except ValueError:
            raise ValueError(f"{filename} doesn't log total lines cleared")

    return total_frames, lines_cleared, data

# example usage
if __name__ == '__main__':
    data_file = input('please input the path to a test replay file: \n>>> ')
    if not os.path.exists(data_file) or not data_file.endswith('.rep'):
        print('invalid data file')
        sys.exit(1)
    
    total_frames, lines_cleared, data = get_file_info(data_file)
    print(list(data))
