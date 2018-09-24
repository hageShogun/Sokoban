from functools import reduce
import copy
import numpy as np

class Sokoban:
    digit2ch = {0: ' ', 1: '#', 2: '@', 3: '$', 4: '.', 5: '+', 6: '*'}
    ch2digit = {' ': 0, '#': 1, '@': 2, '$': 3, '.': 4, '+': 5, '*': 6}
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    ch2move = {'u': 0, 'd': 1, 'l': 2, 'r': 3}

    def __init__(self):
        self.state = None
        self.size = None  # (size_x, size_y)
        self.player = None
        self.goals = []

    def load_level_from_file(self, fname, mode):
        '''
        fname(str): file name of the level.
        mode(str): 'digit' or 'ch'
        '''
        with open(fname) as f:
            s = f.read().rstrip()
            self.load_level_from_str(s, mode)

    def load_level_from_str(self, level_str, mode):
        '''
        level_str(str): level described in string.
        mode(str): 'digit' or 'ch'
        '''
        self.state = level_str.split('\n')
        if mode == 'ch':
            self.state = self.convert_to_digit(self.state)
        elif mode == 'digit':
            # state is converted from ['123', '456', ...] to [[1,2,3], [4,56],.]
            self.state = list(map(lambda x: list(map(int, x)),\
                                  map(list, self.state)))
        
        # Parse level
        sy = len(self.state)
        sx = reduce(lambda x, y: len(y) if x < len(y) else x, self.state, -1)
        self.size = (sx, sy)

        n_box, n_goal, n_player = 0, 0, 0
        for y, row in enumerate(self.state):
            '''
            If the length of a row is smaller than the maximum length
            of the level, the wall is added to the end of the row.
            '''
            t = sx - len(row)
            if 0 < t:
                row.extend([1]*t)
            for x, digit in enumerate(row):
                if digit == 2:  # palyer
                    self.player = [x, y]
                    n_player += 1
                elif digit == 3:  # box
                    n_box += 1
                elif digit == 4:  # goal
                    self.goals.append((x, y))
                    n_goal += 1
                elif digit == 5:  # palyer on a goal
                    self.player = [x, y]
                    self.goals.append((x, y))
                    self.state[y][x] = 2
                    n_goal += 1
                elif digit == 6:
                    self.goals.append((x, y))
                    self.state[y][x] = 3
                    n_box += 1

        # check the validation
        if self.player is None:
            print('The given level does not include a player.')
            sys.exit(1)
        elif n_player > 1:
            print('The given level includes multiple players.')
            sys.exit(1)
        elif n_goal == 0:
            print('The given level does not include any goals.')
            sys.exit(1)
        elif n_goal != n_box:
            print('The numbers of box and goal does not match.')
            sys.exit(1)

    def step(self, move_dir):
        '''
        move_dir(str/int):A Direciton of the movement which is in 'udlr' or 0..3.
        '''
        if move_dir in 'udlr':
            move_dir = Sokoban.ch2move[move_dir]
        move = Sokoban.moves[move_dir]

        future_pos1 = (self.player[0]+move[0], self.player[1]+move[1])
        future_pos2 = (self.player[0]+2*move[0], self.player[1]+2*move[1])

        if future_pos1[0] < 0 or future_pos1[1] < 0 or \
           future_pos1[0] >= self.size[0] or future_pos1[1] >= self.size[1] or \
           self.state[future_pos1[1]][future_pos1[0]] == 1:
            # Player simply can't move due to a wall or limit of level.
            return self.state, 0, False, ''
        elif self.state[future_pos1[1]][future_pos1[0]] == 3 and \
             self.state[future_pos2[1]][future_pos2[0]] in [1, 3]:
            # Player also can't move due to stacking of a box.
            return self.state, 0, False, ''
        else:
            # A box is moved.
            if self.state[future_pos1[1]][future_pos1[0]] == 3:
                self.state[future_pos2[1]][future_pos2[0]] = 3
            if (self.player[0], self.player[1]) in self.goals:
                # Player is moved from a goal.
                self.state[self.player[1]][self.player[0]] = 4
            else:
                self.state[self.player[1]][self.player[0]] = 0
            self.state[future_pos1[1]][future_pos1[0]] = 2
            self.player = [future_pos1[0], future_pos1[1]]
            done = self.check_done()
            print(done)
            return self.state, 0, done, ''

    def check_done(self):
        for goal in self.goals:
            if self.state[goal[1]][goal[0]] != 3:
                return False
        return True
            
    def convert_to_digit(self, state):
        '''
        state(str): ["####", "#  @#", ...]
        '''
        return list(map(lambda x:\
                        list(map(lambda y: Sokoban.ch2digit[y], x)), state))

    def convert_to_ch(self, state):
        '''
        state(2d-list): [[0, 0, 0], [0, 1, 0], ...]
        '''
        return list(map(lambda x:\
                        list(map(lambda y: Sokoban.digit2ch[y], x)), state))

    def render(self):
        state_ch = self.convert_to_ch(self.state)
        for row in state_ch:
            for ch in row:
                print(ch, end='')
            print('')
    

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--level', action='store', type=str)
    parser.add_argument('--mode', action='store', type=str)

    args = parser.parse_args()

    level='''\
#######
#     #
#     #
#. #$ #
#.$   #
#.$$  #
#.#  @#
#######'''

    game = Sokoban()
    if args.level is not None:
        if args.mode is None:
            print('You must assign mode for parsing the given level.')
            sys.exit(1)
        game.load_level_from_file(args.level, mode=args.mode)
    else:
        print('Example level is started.')
        game.load_level_from_str(level, mode='ch')

    done = False
    game.render()
    while not done:
        move_dir = input('Please input (u,d,l,r, or q):')
        if not (move_dir in 'udlrq') or move_dir == '':
            print('Unknown character is input.')
            continue
        if move_dir == 'q':
            print('Good Bye !')
            sys.exit(0)
        state, r, done, info = game.step(move_dir)
        game.render()
