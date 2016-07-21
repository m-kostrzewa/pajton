from snake_segment import SnakeSegment
import curses
from point import Point
import colors

class SnakeHead(SnakeSegment):

    def __init__(self, position):
        super().__init__(position)
        self.last_position = position.copy()
        
        
    def advance(self, new_pos):
        self.last_position = self.position.copy()
        super().advance(new_pos)


    def draw(self, pad):
        to_draw = self.determine_head_character()
        pad.addstr(self.position.y, self.position.x, to_draw, 
            curses.color_pair(colors.snake_color_pair))
        if self.next_segment is not None:
            self.next_segment.draw(pad)
            
            
    def determine_head_character(self):
        delta = self.position.subtract(self.last_position)
        if delta.x > 0 and delta.y == 0:
            return ">"
        elif delta.x < 0 and delta.y == 0:
            return "<"
        elif delta.x == 0 and delta.y > 0:
            return "v"
        else: 
            return "^"