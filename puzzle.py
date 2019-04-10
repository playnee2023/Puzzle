import json
import os.path
import random
import argparse

RawData = 'words.txt'
Dictionary = 'dictionary.txt'


class Trie(object):
    def __init__(self):
        self.root = {}
        self.end = 'end'

    def insert(self, word: str):
        """
        :param word:
        :return: None
        """
        cur_node = self.root
        for c in word:
            if c not in cur_node:
                cur_node[c] = {}
            cur_node = cur_node[c]
        cur_node[self.end] = True

    def prefix(self, word: str):
        """
        Check if the given word is prefix of existing words in dictionary
        :param word:
        :return: The node stores the last character of the given word if there is any, otherwise None
        """
        cur_node = self.root
        for c in word:
            if c not in cur_node:
                return
            cur_node = cur_node.get(c, [])

        return cur_node


def create_dictionary():
    """
    Generate dictionary file with the provided raw data
    :return:
    """
    dictionary = Trie()
    raw_file = os.path.join(os.path.curdir, RawData)
    with open(raw_file, 'rt') as f:
        words = f.readlines()
        for word in words:
            word = word[:-1]
            if len(word) > 1:
                dictionary.insert(word.lower())

    words_file = os.path.join(os.path.curdir, Dictionary)
    with open(words_file, 'wt') as f:
        f.write(json.dumps(dictionary.root))

    # Check if all words can be found
    dictionary = Trie()
    with open(os.path.join(os.path.curdir, Dictionary), 'rt') as f:
        dictionary.root = json.loads(f.read())

    for w in words:
        w = w[:-1]
        if len(w) > 1 and not dictionary.prefix(w)[dictionary.end]:
            print(w)


def create_board(n: int):
    """
    Randomly generate a n x n game board
    :param n: n > 0
    :return: [n][n] game board
    """
    seq = 'abcdefghijklmnopqrstuvwxyz'
    board = []
    for i in range(n):
        row = [random.choice(seq) for _ in range(n)]
        board.append(row)

    return board


def sequence_generator(board: list):
    """
    Generator for all word sequence in forward, backward, downward, upward and diagonal
    :param board: a n x n game board
    :return:
    """
    n = len(board[0])
    for i in range(n):
        sequence = [
            board[i][:],  # forward
            [x for x in reversed(board[i][:])],  # backward
            [board[x][i] for x in range(n)],  # downward
            [board[x][i] for x in range(n - 1, -1, -1)],  # upward
        ]
        if i == 0:
            # diagonals
            diagonal_0 = [board[x][x] for x in range(n)]
            sequence.append(diagonal_0)
            sequence.append([diagonal_0[x] for x in range(n - 1, -1, -1)])
            diagonal_1 = [board[x][n - x - 1] for x in range(n)]
            sequence.append(diagonal_1)
            sequence.append([diagonal_1[x] for x in range(n - 1, -1, -1)])
        yield from sequence


def word_hunting(board: list):
    """
    Find all valid words from a randomly generated n x n game board
    :param board: n x n game board, n > 0
    :return:
    """
    result = []
    table = Trie()
    n = len(board[0])
    with open(os.path.join(os.path.curdir, Dictionary), 'rt') as f:
        table.root = json.loads(f.read())

    for row in sequence_generator(board):
        left = 0
        right = 1
        while left < n and right <= n:
            cur = ''.join(row[left:right])
            node = table.prefix(cur)
            if node is None:
                left += 1
                right = left + 1
            else:
                right += 1
                if table.end in node:
                    result.append(cur)

    return list(set(result))


def show_result(board: list, values: list):
    print('\n--------------- Game Board ---------------')
    for i in board:
        print(i)
    print('\n--------------- Valid Words ---------------')
    for v in values:
        print(v)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='check_words, get_board, menu')
    parser.add_argument('dimension', nargs='?', help='the dimension of the game board', type=int)
    args = parser.parse_args()

    if args.command == 'menu':
        print('\n----------------------------- Example ------------------------------:\n')
        print('Check words for a 15x15 game board:    python puzzle.py check_words 15')
        print('Create a 15x15 game board:             python puzzle.py get_board 15')
    else:
        if args.dimension is None:
            print('Please provide the dimension of the game board')
            exit(1)

        if args.command == 'get_board':
            for r in create_board(args.dimension):
                print(r)

        if args.command == 'check_words':
            game_board = create_board(args.dimension)
            results = word_hunting(game_board)
            show_result(game_board, results)
