# -*- coding: utf-8 -*-
"""

code taken from https://github.com/korolvs/snake_nn/blob/master/snake_game.py
find explanation here:
https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3
"""


# import packages
import argparse
import curses
from random import randint
import numpy as np

# define classes
class SnakeGame:
    def __init__(self, board_width=20, board_height=20, game_steps=50,
                 gui = False):
        '''Class initiation

        Arguments:
        - board_width: int, width of game field
        - boad_height: int, height of game field
        - game_steps: int, length of game
        - gui: bool, if set GUI is used via curses

        '''

        self.score = 0
        self.time = 0
        self.game_steps = game_steps
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
        self.end = ''

    def start(self):
        '''Starting procedure of the game
        '''
        self.snake_init()
        self.generate_food()
        if self.gui: 
            self.render_init()
        return self.generate_observations()

    def snake_init(self, start_box=5):
        '''Initialize the snake body

        Arguments:
        - start_box: int, edge width in which snake does NOT start

        '''

        # determine starting position
        x = randint(start_box, self.board["width"] - start_box)
        y = randint(start_box, self.board["height"] - start_box)

        # create snake body
        self.snake = []
        vertical = randint(0,1) == 0

        for i in range(3):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)
        direction = np.array(self.snake[0])-np.array(self.snake[1])
        self.direction = self.vec_to_key(direction)
    
    def vec_to_key(self, vec):
        if np.array_equal(vec, np.array([1,0])):
            key = 107 # DOWN
        elif np.array_equal(vec, np.array([-1,0])):
            key = 105 # UP
        elif np.array_equal(vec, np.array([0,1])):
            key = 108 # RIGHT
        elif np.array_equal(vec, np.array([0,-1])):
            key == 106 # LEFT
        else:
            raise Exception('Wrong direction')
        return key
    
    def opposite(self, key):
        '''Function to return opposide direction of key

        Arguments:
        - key: int, direction encoded in integer

        '''

        mapping = {105: 107, 106: 108, 107: 105, 108: 106}
        return mapping[key]
    
    def generate_food(self):
        '''Function to place food at a random position in game field
        '''

        food = []
        while food == []:
            food = [randint(1, self.board["width"]),
                    randint(1, self.board["height"])]

            # do not place food into snake, duh!
            if food in self.snake: 
                food = []
        self.food = food

    def render_init(self):
        '''Function to initiate curses screen
        '''

        curses.initscr()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        #win.nodelay(True)
        win.timeout(200)
        self.win = win
        self.render()

    def render(self):
        '''Render curses session
        '''

        self.win.clear()
        self.win.border(0)
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addstr(0, 12, 'Dir: ' + str(chr(self.direction)))
        #self.win.addch(self.food[0], self.food[1], '🍎')
        self.win.addch(self.food[0], self.food[1], '$')
        for i, point in enumerate(self.snake):
            if i == 0:
                #self.win.addch(point[0], point[1], '🔸')
                self.win.addch(point[0], point[1], 'O')
            else:
                #self.win.addch(point[0], point[1], '🔹')
                self.win.addch(point[0], point[1], 'x')
        #self.win.getch()

    def step(self, key):
        '''Function to proceed game for one step

        Arguments:
        - key: int, direction encoded as integer

        '''

        # check if ending condition is fulfilled
        if self.done == True: 
            self.end_game()

        # continue direction if no key is pressed or key points backwards
        if (key == -1
            or key == self.opposite(self.direction)
            or key not in [105, 106, 107, 108]):
            key = self.direction
        # otherwise store direction of key
        else: 
            self.direction = key

        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()

        # condition check
        self.check_collisions()
        self.check_game_steps()

        if self.gui: 
            self.render()

        # set in-game time +1
        self.time += 1

        return self.generate_observations()

    def create_new_point(self, key):
        '''Function to extend snake body

        Arguments:
        - key: int, direction encoded as int

        '''

        new_point = [self.snake[0][0], self.snake[0][1]]
        if key == 105:
            new_point[0] -= 1 # UP
        elif key == 108:
            new_point[1] += 1 # RIGHT
        elif key == 107:
            new_point[0] += 1 # DOWN
        elif key == 106:
            new_point[1] -= 1 # LEFT
            
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        '''function to check for collisions
        '''

        if (self.snake[0][0] == 0 or
            self.snake[0][0] == self.board["width"] + 1 or
            self.snake[0][1] == 0 or
            self.snake[0][1] == self.board["height"] + 1 or
            self.snake[0] in self.snake[1:-1]):
            self.done = True
            self.end = 'Snake ran against something!'

    def check_game_steps(self):
        '''Function to check in-game time
        '''

        if self.time == self.game_steps:
            self.done = True
            self.end = 'Game time is up ({})!'.format(self.game_steps)

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        if self.gui: 
            self.render_destroy()
        #print(self.snake)
        #print(self.direction)
        print(self.end)
        exit()
        #raise Exception(self.end)

if __name__ == "__main__":
    # parsing command line arguments
    parser = argparse.ArgumentParser(description= \
        'Basic snake game. Can be played within bash via the curses package. \
         The snake can be controlled via i (up), j (left), k (down), l \
         (right).')
    parser.add_argument('--game_steps', type=int, default=100,
        help='An integer to define the length of the game.')

    args = parser.parse_args()
    GAME_STEPS = args.game_steps

    # running the game
    game = SnakeGame(game_steps=GAME_STEPS, gui=True)
    game.start()
    while True:
        input_key = game.win.getch()
        game.step(input_key)