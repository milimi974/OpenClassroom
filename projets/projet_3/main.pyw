""" Import dependences. """
from random import randrange # Import méthod from random module for make range value
import time # Import module time for pass game on pause
import json # Import json module

import pygame # Import Pygame Module

class ConstClass(object):
    """ That a class contain all constant for the game. """
    # Settings constant game map
    MAP_COLUMN = 15 # Grid column size
    MAP_ROW = 15 # Grid row size
    CELL_WIDTH = 21 # Grid cell Width
    CELL_HEIGHT = 21 # Grid cell Height
    MAP_ITEMS = ["5", "6", "7"] # Lis of items ID    
    ITEMS_SPACE = 2 # Distance between items

    # Settings constant game hero
    SPRITE = "./assets/hero.png" # Defined hero sprite
    SPRITE_WIDTH = 21 # Sprite Width
    SPRITE_HEIGHT = 21 # Sprite Height

    # Settings constant game screen
    SCREEN_WIDTH = 640 # Game screen width size
    SCREEN_HEIGHT = 480 # Game screen height size    
    GAME_SCREEN_NAME = "MacGyver Escape RoOm" # Game screen name
    GAME_SCREEN_BACKGROUND = (0, 0, 0) # Game screen background color    
    FPS = 24 # Framerate screen

    # Override setter to lock value change
    def __setattr__(self, **kwargs):
        pass

# Instanciate Object contain all constant
CONST = ConstClass()

class Map:
    """ That Class manage map. """    

    def __init__(self, screen_width, screen_height):
        """ Initialize the Map object.
        Keyword arguments:
        screen_width -- Integer Pygame screen size width
        screen_height -- Integer Pygame screen size Height

        """
        # Initialize a list that contains the map data
        self.map = [[0 for x in range(CONST.MAP_COLUMN)] for x in range(CONST.MAP_ROW)]
        # Centred map in game screen
        self.map_x = (screen_width - (CONST.MAP_COLUMN*CONST.CELL_WIDTH))/2
        self.map_y = (screen_height - (CONST.MAP_ROW*CONST.CELL_HEIGHT))/2
        # Initialize hero spawn point position
        self.spawn_point_x = 0
        self.spawn_point_y = 0
        self.map_sprite = {} # Dictionnary for all map items/object description
        # Load map sprite
        self.__load_sprite()
        # Load the first map
        self.load_map(1)

    def load_map(self, map):
        """ Initialize a new map.
        Keyword arguments:
        map -- Integer Map number

        """
        # Create the map filename
        map_filename = "level_" + str(map) + ".txt"
        # Opening the file and create a list that contain each line
        file_list = open(map_filename).read().splitlines()
        # var for identify row position
        row = 0
        # Loop iterate all line
        for line in file_list:
            # Create a new list that contain all cell value
            line_list = line.split(',')
            # Loop for identify the column et and cell value from the list
            for column, cell in enumerate(line_list):
                # Set map cell with the new value identify by row and column
                self.make_cell(row, column, cell)
                # Initialise spawn point position
                if(str(cell) == "2"):
                    self.spawn_point_x = column
                    self.spawn_point_y = row
            row += 1
        # Create all items on map
        self.__make_items()

    def make_cell(self, row, column, item):
        """ Change cell value on the map.
        Keyword arguments:
        row -- Integer Map row position
        column -- Integer Map column position
        cell -- String Map cell value

        """
        self.map[row][column] = str(item)

    def read_cell(self, row, column):
        """ Return cell value on the map.
        Keyword arguments:
        row -- Integer Map row position
        column -- Integer Map column position

        """
        return self.map[row][column]

    def draw(self, screen):
        """ Draw the map sprite on the screen.
        Keyword arguments:
        screen -- Object Screen reference

        """
        # Loop iterate map list to get back cell value identify by row, column position
        for col in range(0, CONST.MAP_ROW):
            for row in range(0, CONST.MAP_COLUMN):
                # Read cell value at the row, column position
                cell = self.read_cell(row, col)
                # Create an object image from cell value
                image = self.make_image(cell)
                if image:
                    # Show image on the screen if exist
                    screen.blit(
                        image,
                        (
                            self.map_x + (col*CONST.CELL_WIDTH),
                            self.map_y + (row*CONST.CELL_HEIGHT)
                        ))

    def update(self):
        """ Update map actions before draw."""
        pass

    # Methode public read sprite message to display
    def read_message(self, cell):
        """ Return sprite message to display on screen.
        Keyword arguments:
        cell -- integer Cell value

        """
        # Identify if message exist on MAP_SPRITE
        if str(cell) in self.map_sprite:
            if "gui_message" in self.map_sprite[str(cell)]:
                return self.map_sprite[str(cell)]["gui_message"]
        return False

    def make_image(self, cell):
        """ Return an image object for the cell value.
        Keyword arguments:
        cell -- integer Cell value

        """
        # Identify if cell sprite exist on map_sprite
        if str(cell) in self.map_sprite:
            sprite = self.map_sprite[str(cell)]['image']
            # Use pygame for create an image object
            return pygame.image.load(sprite)
        return False

    # Methode private set items on map
    def __make_items(self):
        """ Random creation of items on the map."""
        # List contain tulpes position of already created item
        rand_values = []
        # Loop iterate items value
        for item in CONST.MAP_ITEMS:
            # Variable for break/stop loop
            item_add = False
            # Loop execute action until item_add change to True
            while not item_add:
                # Random a row, column value to 0 at max row,column size
                row = randrange(0, CONST.MAP_ROW)
                col = randrange(0, CONST.MAP_COLUMN)
                # Read cell value identify at row, column
                cell = self.read_cell(row, col)
                # Check if can create item
                if(cell == "0" and self.__can_draw_item(rand_values, row, col)):
                    # Create item at row, column
                    self.make_cell(row, col, item)
                    # Stock a tuple position of new item
                    rand_values.append((col, row))
                    # Exit Loop
                    item_add = True

    def __can_draw_item(self, rand_values, row, col):
        """ Return if can draw an item.
        Keyword arguments:
        rand_values -- List[Tulpe] Existing item
        row -- Integer Row position on the map
        col -- Integer Column position on the map

        """
        # Answer to return
        can = True
        # Loop iterate existing item position and compare to new one
        for val in rand_values:
            x, y = val
            # Item can't be created if is position are inside range defined
            if (x > col-CONST.ITEMS_SPACE and x < col+CONST.ITEMS_SPACE) or\
               (y > row-CONST.ITEMS_SPACE and y < row+CONST.ITEMS_SPACE):
                can = False
                break
        return can

    def __load_sprite(self):
        """ Load sprite file then initialise sprite object. """
        with open('sprites.json', 'r', encoding='utf8') as data_file:
            self.map_sprite = json.load(data_file)

    @property
    def spawn_point(self):
        """ Return Tulpe of spawn point position. """
        return (self.spawn_point_x, self.spawn_point_y)

    @property
    def map_position(self):
        """ Return Tylpe of map position. """
        return (self.map_x, self.map_y)

    @property
    def map_items(self):
        """ Return List of items list. """
        return CONST.MAP_ITEMS

class Hero:
    """ That class manage hero. """    

    def __init__(self, name, spawn_position, map_position):
        """ Initialize the Hero object.
        Keyword arguments:
        name -- String Hero name
        spawn_position -- Tulpe Hero start position
        map_position -- Tulpe map_position on screen

        """
        self.name = name
        self.spawn_position = spawn_position
        self.x, self.y = spawn_position
        self.map_x, self.map_y = map_position
        # Initialise Hero sprite image object
        self.image = pygame.image.load(CONST.SPRITE)

    def draw(self, screen):
        """ Draw Hero on the screen.
        Keyword arguments:
        screen -- Object Screen reference

        """
        screen.blit(
            self.image,
            (
                self.map_x + (self.x*CONST.SPRITE_WIDTH),
                self.map_y + (self.y*CONST.SPRITE_HEIGHT)
            ))

    def update(self, x, y):
        """ Update Hero status.
        Keyword arguments:
        x -- Integer Hero x position on map
        y -- Integer Hero y position on map

        """
        # Change Hero position to x, y
        self.__move(x, y)

    def __move(self, x, y):
        """ Move Hero position to x, y.
        Keyword arguments:
        x -- Integer Hero x position on map
        y -- Integer Hero y position on map

        """
        # Update Hero current by add new postion value
        self.x += x
        self.y += y

    @property
    def hero_position(self):
        """ Return Tulpe contain Hero position. """
        return (self.x, self.y)

    @property
    def hero_name(self):
        """ Return String contain Hero name. """
        return self.name

class GameController:
    """ That class are the heart of the game. """    

    def __init__(self):
        """ Initialize the GameController object. """
        pygame.init() # Pygame initialization
        # Create a new window with size 640 x 480 "width x height"
        self.screen = pygame.display.set_mode((CONST.SCREEN_WIDTH, CONST.SCREEN_HEIGHT))
        # Set screen name
        pygame.display.set_caption(CONST.GAME_SCREEN_NAME)

        # Game keypress action Horizontal x Vertical y
        # value -1 0 1 for x left not move right same for y up not move down
        self.move_x = 0
        self.move_y = 0
        # Instanciate Map
        self.map = Map(CONST.SCREEN_WIDTH, CONST.SCREEN_HEIGHT)
        # Instanciate Hero
        self.hero = Hero("Mc Guyver", self.map.spawn_point, self.map.map_position)
        # Initialise object attributes
        self.key_door = False # Bool for statu key found
        self.items = [] # List contain items found
        self.game_over = False # Bool statu game hover
        self.game_end = False # Bool game ending
        self.game_closed = False # Game status
        self.clock = pygame.time.Clock() # Initilise object manage game time
        self.message = "" # Message to show on screen
        self.message_time = 0 # Time message appear on screen

    def game_start(self):
        """ Launch game Loop. """
        # Main Loop execute game until game_closed are false
        while not self.game_closed:
            # Update clock game time by framerate
            self.clock.tick(CONST.FPS)
            # Call method listen keyboard event
            self.__gamepad()
            # Method call all object.update() or method to update
            self.__update(self.clock.get_time())
            # Refresh screen background color
            self.screen.fill(CONST.GAME_SCREEN_BACKGROUND)
            # Method updated all object.draw() or method to draw
            self.__draw(self.clock.get_time())
            # Pygame windows refresh
            pygame.display.update()
            # Game event stop are activate
            if self.game_end:
                # Methode call before ending game
                self.__game_end(self.clock.get_time())
        # Leaved game
        self.__quit();

    def __game_end(self, dt):
        """ Execute action before stop game.
        Keyword arguments:
        dt -- integer Deltatime time between 2 update Main Loop

        """
        # pause game 3sec
        time.sleep(3)
        # Exit Main Loop
        self.game_closed = True

    def __update(self, dt):
        """ call all object.update() or method to update before draw.
        Keyword arguments:
        dt -- integer Deltatime time between 2 update Main Loop

        """
        # Event collision
        self.__update_collision()
        # Update Map
        self.map.update()
        # Update Hero
        self.hero.update(self.move_x, self.move_y)
        # Update Message time display
        self.__update_message(dt)

    def __update_message(self, dt):
        """ Update screen message time appears.
        Keyword arguments:
        dt -- integer Deltatime time between 2 update Main Loop

        """
        if self.message:
            if self.message_time <= 1000:
                self.message_time += dt
            else:
                self.message_time = 0
                self.message = None

    def __update_collision(self):
        """ Check if have a collision. """
        # Read cell of next postion of Hero on the map
        cell = self.map.read_cell(*self.next_position)
        # if collision with somthing else ground
        if(cell != "0"):
            # Call event collision by cell type
            self.__event_collision(cell)

    def __event_collision(self, cell):
        """ Make action on cell type ID.
        Keyword arguments:
        cell -- String cell ID

        """
        # Event for collision with wall
        if cell == "1":
            self.move_x = 0
            self.move_y = 0

        # Event for collision with door
        elif cell == "9":
            if self.key_door: # Key found
                # Message to show
                self.message = "a ouvert la porte."
                # Change cell image by ground
                self.map.make_cell(*self.next_position, "0")
                # Reste key found
                self.key_door = False

            else: # Key not found
                # Message to show
                self.message = self.map.read_message(cell)
                # Reset Next move
                self.move_x = 0
                self.move_y = 0

        # Event for collision with key
        elif cell == "8":
            # Message to show
            self.message = self.map.read_message(cell)
            # Change cell image by ground
            self.map.make_cell(*self.next_position, "0")
            # Key found
            self.key_door = True

        # Event for collision with items
        elif cell in self.map.map_items:
            # Message to show
            self.message = self.map.read_message(cell)
            # Change cell image by ground
            self.map.make_cell(*self.next_position, "0")
            # Add item found
            self.items.append(cell)

        # Event for level ended
        elif cell == "-1":
            # Ending game level
            self.game_end = True
            # Message to show
            self.message = "Niveau terminé !!!"

        # Event for collision with enemy
        elif cell == "3":
            if len(self.items) == 3:
                # Message to show
                self.message = self.map.read_message(cell)
                # Change cell image by ground
                self.map.make_cell(*self.next_position, "0")

            else:
                # Message to show
                self.message = "meurt sans pouvoir rien faire ..."
                # Ending game GameOver
                self.game_end = True

    @property
    def next_position(self):
        """ Return Tulpe contain next position move of Hero. """
        # Get Hero current position
        x, y = self.hero.hero_position
        # Add current positionwith next move position
        return(y+self.move_y, x+self.move_x)

    def __draw(self, dt):
        """ call all object.draw() or method to draw element on screen.
        Keyword arguments:
        dt -- integer Deltatime time between 2 update Main Loop

        """
        # Draw Map on screen
        self.map.draw(self.screen)
        # Draw Hero on screen
        self.hero.draw(self.screen)
        # Draw Game GUI
        self.__draw_gui()
        # Draw message
        self.__draw_message(dt)

    def __draw_message(self, dt):
        """ Draw a message on the screen.
        Keyword arguments:
        dt -- integer Deltatime time between 2 update Main Loop

        """
        if self.message:
            # Compose message with hero name
            message = self.hero.hero_name + " " + self.message
            # Define text font size with default font
            Font = pygame.font.Font(None, 30)
            # Get message box object
            text_surface = Font.render(message, True, (0, 128, 255))
            # Get message box size
            rect_text = text_surface.get_rect()
            # Set text centred position
            rect_text.center = self.map.map_x*2, self.map.map_y-25
            # Draw message on screen
            self.screen.blit(text_surface, rect_text)

    def __draw_gui(self):
        """ Draw GUI on the screen. """
        img = None
        if self.key_door: # Draw image for key found
            img = pygame.image.load("./assets/gui_key_on.png")
        else: # Draw image for key not found
            img = pygame.image.load("./assets/gui_key_off.png")
        # get map position
        x, y = self.map.map_position
        # Set position y of image up map
        y -= CONST.CELL_HEIGHT + 1
        # Draw image on screen
        self.screen.blit(img, (x, y))
        # Move next position x to right
        x += CONST.CELL_WIDTH + 2
        # Loop items found
        for item in self.items:
            # Create image object
            img = self.map.make_image(item)
            # Draw image on map
            self.screen.blit(img, (x, y))
            # Move next item position to right
            x += CONST.CELL_WIDTH + 2

    def __gamepad(self):
        """ Event on keybord. """
        # Reste move
        self.move_x = 0
        self.move_y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clic on cross windows
                self.game_closed = True # exit game
            if event.type == pygame.KEYDOWN: # User clic a touch
                if event.key == pygame.K_LEFT: # User clic left
                    self.move_x = -1
                elif event.key == pygame.K_RIGHT: # User clic right
                    self.move_x = 1
                elif event.key == pygame.K_UP: # User clic up
                    self.move_y = -1
                elif event.key == pygame.K_DOWN: # User clic down
                    self.move_y = 1

    def __quit(self):
        """ Leaved game. """
        pygame.quit() # close pygame
        quit() # close script

# instansiate game object
game = GameController()
# Start game
game.game_start()
