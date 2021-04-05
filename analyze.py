import os
import parse

from typing import Callable, List, Tuple, Union

# return the indices where a hard drop happens
def check_hard_drop() -> Callable[[], Union[None, int]]:
    # use closure to keep track of the previous hard drop
    last_key_sum = 0

    def check_hard_drop_inner(enum: Tuple[int, Tuple[int, int]]):
        ret: Union[None, int]
        nonlocal last_key_sum

        (i, entry) = enum
        (frame_num, key_sum) = entry

        if parse.button_held(key_sum, 'hard drop') is True and
           parse.button_held(last_key_sum, 'hard drop') is False:
            ret = i
        else:
            ret = None
        
        last_key_sum = key_sum
        return ret
    
    return check_hard_drop_inner

def get_avg_fbm(sequence: List[Tuple[int, int]]) -> float:
    """
    fbm -> "Frames before moved"
    Finds the average number of frames before a piece is moved for a given game.
    """

    # find all places where a piece is set down
    # note: assumes all pieces are placed with a hard drop
    piece_placements = list(filter(
        lambda entry: entry is not None,
        map(check_hard_drop(), enumerate(sequence))))

    print(piece_placements)
    print(len(piece_placements))

    return
if __name__ == '__main__':
    # data_file = input('please input the path to a test replay file: \n>>> ')
    # if not os.path.exists(data_file) or not data_file.endswith('.rep'):
    #     print('invalid data file')
    #     sys.exit(1)

    data_file = '/mnt/g/Applications/NullpoMino/replay/2021_04_05_13_01_15.rep'
    
    total_frames, lines_cleared, data = parse.get_file_info(data_file)

    get_avg_fbm(list(data))
