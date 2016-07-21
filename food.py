import curses
from point import Point
import colors

class Food:

    def __init__(self, x, y):
        self.position = Point(x, y)
        
        
    def draw(self, pad):
        pad.addstr(self.position.y, self.position.x, "o",
            curses.color_pair(colors.food_color_pair))
        pad.refresh(0, 0, self.position.y, self.position.x, 
            self.position.y, self.position.x)