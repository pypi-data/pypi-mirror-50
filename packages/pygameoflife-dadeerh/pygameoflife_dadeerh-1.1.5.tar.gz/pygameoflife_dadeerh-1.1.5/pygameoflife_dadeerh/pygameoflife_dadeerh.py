import sys
import random
import time

import pygame




class LifeGame:
    def __init__(self, screen_width=640, screen_height=480, cell_size=10, dead_color = (0,0,0), alive_color=(255,255,255), max_fps = 15):
        """
        Initialize grid, set default game state, initialize screen

        :param screen_width: Game window width
        :param screen_height: Game window height
        :param cell_size: Diameter of circles
        :param dead_color: RGB tuple e.g. (255,0,255)
        :param alive_color: RGB tuple e.g. (255,0,255)
        :param max_fps: Framerate cap to limit game speed
        :return: None
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.circle_radius = self.cell_size // 2
        self.dead_color = dead_color
        self.alive_color = alive_color
        self.max_fps = max_fps

        self.screen_size = (self.screen_width, self.screen_height)
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.init_grids()
        self.paused = False
        self.game_over = False
    
    def init_grids(self):
        """
        Create the default active and inactive grid
        :return: None
        """
        self.num_cols = self.screen_width // self.cell_size
        self.num_rows = self.screen_height // self.cell_size

        self.grids = []

        def create_grid():
            """
            Generate an empty 2d grid
            :return: 2D array of 0s
            """
            grid = []
            for c in range(self.num_cols):
                grid.append([])
                for r in range(self.num_rows):
                    grid[-1].append(0)
            return grid
    
        self.grids.append(create_grid())
        self.grids.append(create_grid())

        self.active_grid = 0

        self.randomize_grid()

    def run(self):
        """ 
        Main game loop function

        :return: None
        """
        while True:
            self.handle_events()
            self.clock.tick(self.max_fps)  # set FPS

            if self.game_over:
                return

            if not self.paused:
                self.clear_screen()
                self.draw_grid()
                self.update_generation()
                pygame.display.update()
    

    def handle_events(self):
        """
        Handle the game events

        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == "q" or event.unicode == "Q":
                    self.game_over = True
                elif event.unicode == "s" or event.unicode == "S":
                    self.paused = not self.paused
                elif event.unicode == "r" or event.unicode == "R":
                    self.randomize_grid()
            if event.type == pygame.QUIT:
                self.game_over = True

    def clear_screen(self):
        """
        Fill whole screen with dead color

        :return: None
        """

        self.screen.fill(self.dead_color)
    
    def zero_grid(self):
        """
        Sets the active grid to all 0's

        :return: None
        """
        self.set_grid(0)

    def randomize_grid(self):
        """
        Randomizes the active grid

        :return: None
        """
        self.set_grid()
    
    def set_grid(self, value=None):
        """
        Set an entire grid at once. Set to single value or random 0/1
        
        :param value: Value to set the cell to (0 or 1)
        :return: None
        """

        for idx_col in range(self.num_cols):
            for idx_row in range(self.num_rows):
                if value is None:
                    self.grids[self.active_grid][idx_col][idx_row] = random.choice([0,1])
                else:
                    self.grids[self.active_grid][idx_col][idx_row] = value

    def draw_grid(self):
        """
        Given the grid and cell states draw the cells on the screen
    
        :return: None
        """

        for idx_col in range(self.num_cols):
            for idx_row in range(self.num_rows):
                if self.grids[self.active_grid][idx_col][idx_row] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                pygame.draw.circle(self.screen, 
                                    color,
                                    ((idx_col * self.cell_size + self.circle_radius), idx_row * self.cell_size + self.circle_radius),
                                    self.circle_radius)


    def update_generation(self):
        """
        Updates the state for all cells in the active grid

        :return: None
        """
        inactive_grid = self.inactive_grid()

        for c in range(self.num_cols):
            for r in range(self.num_rows):
                next_gen_state = self.check_cell_neighbors(c,r)
                self.grids[inactive_grid][c][r] = next_gen_state

        self.active_grid = inactive_grid
    
    def inactive_grid(self):
        """ 
        Helper function to return the currently inactive grid
        
        :return: Inactive grid (0/1)
        """
        return (self.active_grid + 1) % 2



    def count_live_neighbors(self, idx_col, idx_row):
        """
        Counts the alive (1) neighbors to given cell

        :param idx_col: Column index
        :param idx_row: Row index
        :return: Number of alive neighbors(0-8)
        """
        alive_neighbors = 0
        for c in range(-1,2):
            for r in range(-1,2):
                if c == 0 and r == 0:
                    continue
                try:
                    alive_neighbors += self.grids[self.active_grid][idx_col + c][idx_row + r]
                except: 
                    pass
        return alive_neighbors

    def check_cell_neighbors(self, idx_col,idx_row):
        """
        Get the n umber of alive neighbor cella nd determine the state of the cell for the next genretaion. Determine whether it lives, dies, or survives

        :param idx_col: The index of the column
        :param idx:row: The index of the row
        :return: Dead (0) or Alive (1)
        """
        num_alive_neighbors = self.count_live_neighbors(idx_col, idx_row)

        if self.grids[self.active_grid][idx_col][idx_row] == 1: #alive
            if num_alive_neighbors < 2: # underpopulated
                return 0
            elif num_alive_neighbors == 2 or num_alive_neighbors == 3: # remain alive
                return 1
            elif num_alive_neighbors > 3:     # overpopulate
                return 0
        elif self.grids[self.active_grid][idx_col][idx_row] == 0: # dead
            if num_alive_neighbors == 3:  # revive
                return 1

        return self.grids[self.active_grid][idx_col][idx_row]
                    

