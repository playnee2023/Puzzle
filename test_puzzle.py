import datetime
import pytest
from puzzle import word_hunting
from puzzle import show_result
from puzzle import create_board


class TestPuzzle(object):
    test_data = [
        ([['s', 't', 'y', 'e', 's'],
          ['0' for _ in range(5)],
          ['0' for _ in range(5)],
          ['0' for _ in range(5)],
          ['0' for _ in range(5)]],
         ['sty', 'stye', 'styes', 'ts'],
         'forward and backward'
         ),
        ([['s'] + ['0' for _ in range(4)],
          ['e'] + ['0' for _ in range(4)],
          ['y'] + ['0' for _ in range(4)],
          ['t'] + ['0' for _ in range(4)],
          ['s'] + ['0' for _ in range(4)]],
         ['sty', 'stye', 'styes', 'ts'],
         'downward and upward'),
        ([['s'] + ['0' for _ in range(4)],
          ['0', 'e', '0', '0', '0'],
          ['0', '0', 'y', '0', '0'],
          ['0', '0', '0', 't', '0'],
          ['0' for _ in range(4)] + ['s']],
         ['sty', 'stye', 'styes', 'ts'],
         'diagonal'),
        ([['0' for _ in range(4)] + ['s'],
          ['0', '0', '0', 'e', '0'],
          ['0', '0', 'y', '0', '0'],
          ['0', 't', '0', '0', '0'],
          ['s'] + ['0' for _ in range(4)]],
         ['sty', 'stye', 'styes', 'ts'],
         'diagonal')
    ]

    @pytest.mark.parametrize('data', test_data)
    def test_correctness(self, data):
        board, expected, msg = data
        words = word_hunting(board)
        words.sort()
        print('\nTesting for {} search...'.format(msg))
        show_result(board, words)
        assert words == expected

    def test_performance(self):
        start = datetime.datetime.now()
        board = create_board(15)
        words = word_hunting(board)
        end = datetime.datetime.now()
        show_result(board, words)
        print('Test starts at {}'.format(start))
        print('Test ends at {}'.format(end))
        assert start + datetime.timedelta(seconds=30) >= end
