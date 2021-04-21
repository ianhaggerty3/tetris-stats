import unittest
import os
import sys

sys.path.append(os.path.abspath('../src/tetris_stats'))
import parse
import analyze

class TestPPSCalc(unittest.TestCase):

    def test_best_files(self):
        # actual pps values displayed in game, from screenshots
        PPS_real = {
            '2018_09_24_11_29_20.rep': 2.1873,
            '2020_02_21_18_42_18.rep': 2.5689,
            '2020_02_21_18_48_09.rep': 2.7429,
            '2021_02_11_15_51_52.rep': 2.9415,
            '2021_02_07_21_27_51.rep': 2.8346,
            '2019_01_10_13_46_12.rep': 2.3659,
        }

        # PPS_real = {
        #     '2020_02_18_23_24_44.rep': 2.5823,
        # }
        
        for file in PPS_real.keys():
            path = os.path.join('./best_replays', file)
            
            game_info = parse.get_file_info(path)
            pps = round(game_info.pps, 4)
            self.assertAlmostEqual(pps, PPS_real[file])


if __name__ == '__main__':
    unittest.main()

