import curses
import time

from snake import Snake
from food_generator import FoodGenerator
import colors, misc


class Game:
        
    def __call__(self, screen):
        self.screen = screen
        self.run_game()
    
    
    def run_game(self): 
        colors.init_color_pairs()
        self.setup_curses()
        self.configure_game_settings()
        self.exit_game = False

        while True:
            if self.exit_game: break
            self.got_rekt = False
            self.paused = False
            
            self.setup_arena()
            self.setup_stats()
            self.snake = self.spawn_default_snake()
            colors.randomize_snake_colors()

            self.main_loop()


    def setup_curses(self):
        curses.curs_set(0)
        self.screen.nodelay(1)
        self.screen.refresh()
            
            
    def configure_game_settings(self):
        self.arena_width = 60
        self.arena_height = misc.console_height
        self.frame_delay = 0.1
        self.food_generator = FoodGenerator(self.arena_width, self.arena_height,
            num_foods_at_same_time = 20, force_change_timeout = 20)
            

    def setup_arena(self):
        self.arena = curses.newpad(self.arena_height, self.arena_width)
        self.arena.bkgd('w', curses.color_pair(colors.background_color_pair))
        self.arena.box()
        self.refresh_arena()

        
    def setup_stats(self):
        self.stats = curses.newwin(self.arena_height, 20, 0, self.arena_width) 
        self.stats.bkgd(' ', curses.color_pair(colors.background_color_pair),)    
        
        
    def spawn_default_snake(self):
        return Snake(int(self.arena_width/2), int(self.arena_height/2), \
            initial_length = 20)
        
                      
    def main_loop(self):
        while True:
            user_input = self.read_input() 
            if self.should_exit_game(user_input): 
                self.exit_game = True
                break
            self.handle_user_meta_inputs(user_input)

            if not self.paused:
                self.snake.handle_user_input(user_input)
                self.update_all()
                if self.is_snake_collision():
                    self.print_game_over_and_wait()
                    break
                self.snake.eat_if_possible(self.food_generator.foods)
                self.draw_all()
                   
            self.refresh_arena()  
            self.redraw_stats()
            
            time.sleep(self.frame_delay)
        
    
    def read_input(self):
        inp = self.screen.getch()
        curses.flushinp()
        return inp


    def should_exit_game(self, user_input):
        if user_input == 27:
            return True
        return False     
        
        
    def handle_user_meta_inputs(self, user_input):
        if user_input == ord('p'):
            self.toggle_pause()
        elif user_input == ord('1'):
            self.frame_delay += 0.01
        elif user_input == ord('2'):
            if self.frame_delay > 0.02: self.frame_delay -= 0.01
        elif user_input == ord('3'):
            self.food_generator.force_change_timeout += 1
        elif user_input == ord('4'):
            if self.food_generator.force_change_timeout > 1:
                self.food_generator.force_change_timeout -= 1
        elif user_input == ord('5'):
            self.food_generator.num_foods_at_same_time += 1
        elif user_input == ord('6'):
            if self.food_generator.num_foods_at_same_time > 1:
                self.food_generator.num_foods_at_same_time -= 1
        elif user_input == ord('0'):
            self.snake.toggle_style()
                
                
    def toggle_pause(self):
        self.paused = not self.paused
        pause_msg = "GAME_PAUSED"
        if self.paused: 
            self.arena.addstr(int(self.arena_height/2), int(self.arena_width/2), \
                "GAME_PAUSED", curses.A_STANDOUT)
        else: 
            self.arena.addstr(int(self.arena_height/2), int(self.arena_width/2), \
                " "*len(pause_msg)) 
        time.sleep(0.1)
                
        
    def update_all(self):
        self.snake.update()
        self.food_generator.update(self.snake.head)
        
        
    def is_snake_collision(self):
        return self.snake.is_collision_with_arena(self.arena_width, \
            self.arena_height) or self.snake.is_collision_with_self()
        
        
    def draw_all(self):
        self.snake.draw(self.arena)
        self.food_generator.draw_foods(self.arena)
        
    
    def print_game_over_and_wait(self):         
        self.arena.addstr(int(self.arena_height/2), int(self.arena_width/2), 
            "YOU_GOT_REKT", curses.A_STANDOUT)
        self.refresh_arena()
        time.sleep(1.0)
        self.screen.getch()
        self.arena.clear()
        
        
    def refresh_arena(self):
        self.arena.refresh(0, 0, 0, 0, self.arena_height, self.arena_width)


    def redraw_stats(self):
        self.stats.clear()
        self.stats.addstr(1, 7, "PYTHON", curses.A_STANDOUT)
        self.stats.addstr(3, 5, "STATS", curses.A_BOLD)
        self.stats.addstr(4, 2, "Score   :")
        self.stats.addstr(4, 10, str(self.snake.length))
        self.stats.addstr(5, 2, "Delay   :")
        self.stats.addstr(5, 10, format(self.frame_delay, '.3f'))
        self.stats.addstr(5, 15,"ms")
        self.stats.addstr(6, 2, "Freq    :")
        self.stats.addstr(6, 10, str(self.food_generator.force_change_timeout))
        self.stats.addstr(7, 2, "Foods   :")
        self.stats.addstr(7, 10, str(self.food_generator.num_foods_at_same_time))
        self.stats.addstr(9, 5, "CONTROLS", curses.A_BOLD)
        self.stats.addstr(10, 2,"Movement: WSAD")
        self.stats.addstr(11, 2,"Exit    : ESC")
        self.stats.addstr(12, 2,"Pause   : P")
        self.stats.addstr(13, 2,"Delay+  : 1")
        self.stats.addstr(14, 2,"Delay-  : 2")
        self.stats.addstr(15, 2,"Freq+   : 3")
        self.stats.addstr(16, 2,"Freq-   : 4")
        self.stats.addstr(17, 2,"Foods+  : 5")
        self.stats.addstr(18, 2,"Foods-  : 6")
        self.stats.addstr(19, 2,"Style   : 0")
        self.stats.box()
        self.stats.refresh()
        
