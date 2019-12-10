# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:14:06 2019

@author: fumo

code taken from https://github.com/korolvs/snake_nn/blob/master/snake_game.py
find explanation here:
https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3
"""

# -*- coding: utf-8 -*- 
import curses
from random import randint
import numpy as np

class SnakeGame:
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0
        self.time = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: 
            self.render_init()
        return self.generate_observations()

    def snake_init(self, start_box=5):
        x = randint(start_box, self.board["width"] - start_box)
        y = randint(start_box, self.board["height"] - start_box)
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
        mapping = {105: 107, 106: 108, 107: 105, 108: 106}
        return mapping[key]
    
    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: 
                food = []
        self.food = food

    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        #win.nodelay(True)
        win.timeout(200)
        self.win = win
        self.render()

    def render(self):
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
        if self.done == True: 
            self.end_game()
        
        # continue direction if no key is pressed or key points backwards
        if key == -1 or key == self.opposite(self.direction):
            key = self.direction
        else: # otherwise store direction
            self.direction = key
        
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()
        self.check_collisions()
        if self.gui: 
            self.render()
        self.time += 1
        return self.generate_observations()

    def create_new_point(self, key):
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
        if (self.snake[0][0] == 0 or
            self.snake[0][0] == self.board["width"] + 1 or
            self.snake[0][1] == 0 or
            self.snake[0][1] == self.board["height"] + 1 or
            self.snake[0] in self.snake[1:-1]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        if self.gui: 
            self.render_destroy()
        print(self.snake)
        print(self.direction)
        raise Exception("Game over")

if __name__ == "__main__":
    game = SnakeGame(gui = True)
    game.start()
    for _ in range(50):
        input_key = game.win.getch()
        game.step(input_key)