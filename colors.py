import curses
from random import randint


background_color_pair = 1
food_color_pair = 2
snake_color_pair = 3


def init_color_pairs():
    curses.init_pair(background_color_pair, curses.COLOR_GREEN, curses.COLOR_BLACK)
    #curses.init_pair(snake_color_pair, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(food_color_pair, curses.COLOR_MAGENTA, curses.COLOR_RED)
    randomize_snake_colors()
    
    
def randomize_snake_colors():
    foreground = random_color_index()
    background = random_color_index()
    while background == foreground:
        background = random_color_index()
    curses.init_pair(snake_color_pair, foreground, background)
    
    
def random_color_index():
    max_color_index = 7
    return randint(0, max_color_index)