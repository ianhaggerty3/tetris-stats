import os
import parse

from typing import Callable, List, Tuple, Union

# the first frame where the game checks for user input after a countdown
FIRST_GAME_FRAME = 100

# return the indices where a hard drop happens
def check_piece_change() -> Callable[[], Union[None, int]]:
    # use closure to keep track of the previous key presses
    last_key_sum = 0

    def check_piece_change_inner(enum: Tuple[int, Tuple[int, int]]):
        ret: Union[None, int]
        nonlocal last_key_sum

        (i, entry) = enum
        (frame_num, key_sum) = entry

        # start the clock whenever pieces change.
        # this means whenever a hard drop happens, or when a hold happens
        if is_new_press(last_key_sum, key_sum, 'hard drop') or \
           is_new_press(last_key_sum, key_sum, 'hold'):
            ret = i
        else:
            ret = None
        
        last_key_sum = key_sum
        return ret
    
    return check_piece_change_inner

def is_new_press(old_sum: int, new_sum: int, action: str) -> bool:
    if parse.button_held(new_sum, action) is True and \
       parse.button_held(old_sum, action) is False:
       return True
    return False

def get_avg_fba(sequence: List[Tuple[int, int]]) -> float:
    """
    fbm -> "Frames before action"
    Finds the average number of frames before a piece is moved for a given game.
    """

    # find all places where a piece is set down
    # note: assumes all pieces are placed with a hard drop
    piece_changes = list(filter(
        lambda entry: entry is not None,
        map(check_piece_change(), enumerate(sequence))))

    # the "reaction time" before player action is measured from the start to
    # the last action. The last action ends the game, so it is not considered
    # TODO: Filter out key presses prior to the actual game time
    move_frames = sequence[0][0] - FIRST_GAME_FRAME
    num_considered = len(piece_changes)
    for change in piece_changes[:-1]:
        initial_frame = sequence[change][0]
        # holding left or right immediately affects the following piece.
        # no other buttons "hold over" like that
        if parse.button_held(sequence[change][1], 'left') is True or \
           parse.button_held(sequence[change][1], 'right') is True:
           action_frame = initial_frame
        else:            
            last_sum = sequence[change][1]
            i = change + 1
            done = False
            while not done:
                current_sum = sequence[i][1]
                if parse.button_held(current_sum, 'left') is True or \
                    parse.button_held(current_sum, 'right') is True:
                   done = True
                elif is_new_press(last_sum, current_sum, 'cw'):
                    done = True
                elif is_new_press(last_sum, current_sum, 'ccw'):
                    done = True
                elif is_new_press(last_sum, current_sum, 'hard drop'):
                    done = True
                elif is_new_press(last_sum, current_sum, 'hold'):
                    done = True
                
                # do not check for soft drop, since it generally doesn't affect
                # the sprint game mode

                i += 1
                last_sum = current_sum

            action_frame = sequence[i - 1][0]

        move_frames += sequence[change + 1][0] - initial_frame
    
    return move_frames / num_considered


    return
if __name__ == '__main__':
    # data_file = input('please input the path to a test replay file: \n>>> ')
    # if not os.path.exists(data_file) or not data_file.endswith('.rep'):
    #     print('invalid data file')
    #     sys.exit(1)

    data_file = '/mnt/g/Applications/NullpoMino/replay/2021_04_05_21_14_08.rep'
    
    total_frames, lines_cleared, data = parse.get_file_info(data_file)

    sequence = list(data)
    avg_fba = get_avg_fba(sequence)
    print(f'average frames before action = {avg_fba}')
    # if multiple button changes happen on one frame, this estimation is not accurate
    print(f'average frames between actions ~= {(total_frames - FIRST_GAME_FRAME) / ((len(sequence) // 2) + 1)}')
    print(f'number of recorded key presses or releases = {len(sequence)}')
    print(f'total frames = {total_frames}')

