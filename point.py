class Point:
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
      
      
    def scale(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
      

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)
        
            
    def subtract(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    
    def copy(self):
        return Point(self.x, self.y)
        
        
    def equals(self, other):
        return self.x == other.x and self.y == other.y
        
        