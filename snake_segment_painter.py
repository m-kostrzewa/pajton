import curses
from point import Point
    
class SnakeSegmentPainter:

    def __init__(self, position_current, position_prev, position_next):
        self.curr = position_current
        self.prev = position_prev
        self.next = position_next
        
        self.lettercodes_to_primitives_no_corners = {
            "LR": curses.ACS_HLINE,     "UD": curses.ACS_VLINE }
        
        self.lettercodes_to_primitives = { 
            "LR": curses.ACS_HLINE,     "UD": curses.ACS_VLINE,
            "LU": curses.ACS_LRCORNER,  "RU": curses.ACS_LLCORNER,
            "LD": curses.ACS_URCORNER,  "RD": curses.ACS_ULCORNER }
        
            
    def determine_character(self):
        if self.prev.equals(self.curr): 
            return None # this happens only when snake spawns
        elif self.next is None:
            return self.determine_based_on_just_prev_segment()
        elif self.next.equals(self.curr):
            return curses.ACS_DIAMOND # this happens only when snake spawns
        else:
            return self.determine_based_on_prev_and_next_segments()
       
       
    def determine_based_on_just_prev_segment(self):
        for lettercode, primitive in self.lettercodes_to_primitives_no_corners.items():
            if self.is_any_neighbours_position(lettercode):
                return primitive
        (delta_prev, delta_next) = self.get_differences_to_neighbours()
        raise ValueError("Unknown combination of neighbours")
            
            
    def determine_based_on_prev_and_next_segments(self):
        for lettercode, primitive in self.lettercodes_to_primitives.items():
            if self.are_both_neighbours_positions(lettercode):
                return primitive
        raise ValueError("Unknown combination of neighbours")
       
       
    def is_any_neighbours_position(self, code):
        for letter in code:    
            if self.exists_neighbour_towards(letter): 
                return True
        return False
    
    
    def are_both_neighbours_positions(self, code):
        for letter in code:
            if not self.exists_neighbour_towards(letter): return False
        return True
            
            
    def exists_neighbour_towards(self, code):
        (delta_prev, delta_next) = self.get_differences_to_neighbours()
        if code == "U" and (delta_prev.y < 0 or delta_next.y < 0): 
                return True
        elif code == "D" and (delta_prev.y > 0 or delta_next.y > 0): 
                return True
        elif code == "L" and (delta_prev.x < 0 or delta_next.x < 0): 
                return True
        elif code == "R" and (delta_prev.x > 0 or delta_next.x > 0): 
                return True
        return False
        
        
    def get_differences_to_neighbours(self):
        delta_prev = self.prev.subtract(self.curr)
        delta_next = Point(0, 0) # dummy value
        if self.next is not None:
            delta_next = self.next.subtract(self.curr)
        return (delta_prev, delta_next)