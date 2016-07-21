from point import Point

class BoundingBox:

    def __init__(self, seed):
        self.top_left = seed.copy()
        self.bottom_right = seed.copy()
        
    def expand(self, point):
        if point.x < self.top_left.x:
            self.top_left.x = point.x
        elif point.x > self.bottom_right.x:
            self.bottom_right.x = point.x
        if point.y < self.top_left.y:
            self.top_left.y = point.y
        elif point.y < self.bottom_right.y:
            self.bottom_right.y = point.y