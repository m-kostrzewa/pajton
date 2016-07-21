from snake_segment import SnakeSegment
from snake_head import SnakeHead
from point import Point
from bounding_box import BoundingBox

class Snake:

    def __init__(self, start_x, start_y, initial_length = 10):
        self.velocity = Point(1, 0)
        self.head = SnakeHead(Point(start_x, start_y))
        self.tail = self.head
        self.length = initial_length
        self.generate_initial_tail(initial_length)


    def generate_initial_tail(self, length):
        for i in range(length):
            self.tail = self.tail.append_segment()


    def handle_user_input(self, pressed_char):
        if pressed_char == ord('w'):
            self.velocity = Point(0, -1)
        elif pressed_char == ord('a'):
                self.velocity = Point(-1, 0)
        elif pressed_char == ord('s'):
                self.velocity = Point(0, 1)
        elif pressed_char == ord('d'):
                self.velocity = Point(1, 0)


    def is_collision_with_arena(self, arena_width, arena_height):
        if self.head.position.x >= arena_width-1 or \
            self.head.position.x <= 0 or \
            self.head.position.y >= arena_height-1 or \
            self.head.position.y <= 0:
            return True
        return False
        
        
    def is_collision_with_self(self):
        first_collidable = self.head.next_segment
        if first_collidable is not None:
            if first_collidable.find_first_at_position(self.head.position) is not None:
                return True
        return False


    def update(self):
        self.last_tail_position = self.tail.position
        new_head_pos = self.head.position.add(self.velocity)
        self.head.advance(new_head_pos)
        
        
    def eat_if_possible(self, foods):
        edible = filter(lambda f: f.position.equals(self.head.position), foods)
        for e in edible:
            self.tail = self.head.append_segment()
            self.length += 1
            self.head.has_gulp = True
            foods.remove(e)
        
       
    def draw(self, pad):
        pad.addstr(self.last_tail_position.y, self.last_tail_position.x, " ")
        self.head.draw(pad)
        
        
    def toggle_style(self):
        self.head.toggle_style()