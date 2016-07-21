import curses
from point import Point
import colors
from snake_segment_painter import SnakeSegmentPainter

class SnakeSegment:

    def __init__(self, position):
        self.position = position
        self.next_segment = None
        self.prev_segment = None
        self.style = 2
        self.has_gulp = False
        
        
    def advance(self, new_pos):
        if self.next_segment is not None:
            self.next_segment.advance(self.position)
        if self.has_gulp: 
            if self.next_segment is not None:
                self.next_segment.has_gulp = True
            self.has_gulp = False
        self.position = new_pos


    def draw(self, pad):
        if self.style == 1:
            pad.addstr(self.position.y, self.position.x, "#",
                curses.color_pair(colors.snake_color_pair))
        else:
            if self.has_gulp:
                to_draw = curses.ACS_DIAMOND
            else:
                painter = SnakeSegmentPainter(self.position, 
                    self.prev_segment.position if self.prev_segment else None,
                    self.next_segment.position if self.next_segment else None)
                to_draw = painter.determine_character()
                if to_draw is None: return
            pad.addch(self.position.y, self.position.x, to_draw,
                curses.color_pair(colors.snake_color_pair))
        if self.next_segment is not None:
            self.next_segment.draw(pad)
            
            
    def toggle_style(self):
        if self.style == 1: self.style = 2
        else: self.style = 1
        if self.next_segment is not None:
            self.next_segment.toggle_style()
           
                
    def append_segment(self):
        if self.next_segment is None:
            self.next_segment = SnakeSegment(self.position)
            self.next_segment.prev_segment = self
            return self.next_segment
        else:
            return self.next_segment.append_segment()
            
            
    def find_first_at_position(self, pos):
        if self.position.equals(pos):
            return self
        elif self.next_segment is not None:
            return self.next_segment.find_first_at_position(pos)
        else: return None