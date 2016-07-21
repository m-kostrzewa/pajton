from random import randint
from food import Food

class FoodGenerator:

    def __init__(self, arena_width, arena_height, num_foods_at_same_time = 3,
        force_change_timeout = 20):
        self.empty_width = arena_width - 2 # subtact borders
        self.empty_height = arena_height - 2
        self.num_foods_at_same_time = num_foods_at_same_time
        self.foods = []
        self.turns_since_last_change = 0
        self.force_change_timeout = force_change_timeout
        self.expired_foods_positions = []
        
        
    def update(self, snake_head):
        self.expired_foods_positions = []
        self.turns_since_last_change += 1
        if self.turns_since_last_change >= self.force_change_timeout:
            self.expire_random_food()
        while len(self.foods) < self.num_foods_at_same_time:
            self.generate_new_food(snake_head)
            
            
    def expire_random_food(self):
        rand_idx = randint(0, len(self.foods) - 1)
        self.expired_foods_positions.append(self.foods[rand_idx].position)
        del self.foods[rand_idx]
            
            
    def generate_new_food(self, snake_head):
        self.turns_since_last_change = 0
        food_positions = [f.position for f in self.foods]
        while True:
            food = Food(randint(1, self.empty_width), randint(1, self.empty_height))
            if food.position not in food_positions and \
                    snake_head.find_first_at_position(food.position) is None:
                return self.foods.append(food)
            
            
    def draw_foods(self, pad):
        for pos in self.expired_foods_positions:
            pad.addstr(pos.y, pos.x, " ")
        for f in self.foods:
            f.draw(pad)