import pygame # Import Pygame Module
import json # Import json module
import ast # Import ast Module
from random import randrange

class Map:
    MAP_COLUMN = 15 # Grid column size
    MAP_ROW = 15 # Grid row size
    CELL_WIDTH = 21 # Grid cell Width
    CELL_HEIGHT = 21 # Grid cell Height
    MAP_ITEMS = ["5","6","7"]
    MAP_SPRITE = {}
    ITEMS_SPACE = 2 # Distance between items

    # Constructor
    def __init__(self,screen_width,screen_height):
        # init map list
        self.map = [[0 for x in range(self.MAP_COLUMN)] for x in range(self.MAP_ROW)]
       
        # Centred map in game screen
        self.map_x = (screen_width - (self.MAP_COLUMN * self.CELL_WIDTH))/2 
        self.map_y = (screen_height - (self.MAP_ROW * self.CELL_HEIGHT))/2 
        self.spawn_point_x = 0
        self.spawn_point_y = 0

        self.__load_sprite()
        self.load_map(1)

    # Methode public for create a new map
    def load_map(self,map):
        map_filename = "level_"+str(map)+".txt"
        with open(map_filename, "r") as f:            
            row = 0
            for line in f:
                line_list = ast.literal_eval(line)                
                for column, cell in enumerate(line_list):  
                    self.make_cell(row,column,cell)
                    if(str(cell) == "2"):                        
                        self.spawn_point_x = column
                        self.spawn_point_y = row
                row += 1
        self.__make_items()
        
    
    # Methode public change cell value
    def make_cell(self,row,column,item): 
        self.map[row][column] = str(item)

    # Methode public check element on a position
    def read_cell(self,row,column):
        return self.map[row][column]

    # Methode public drawing the map
    def draw(self,screen):
        for col in range(0,self.MAP_ROW):
            for row in range(0,self.MAP_COLUMN): 
                cell = self.read_cell(row,col)
                image = self.__make_image(cell)
                if image:
                    screen.blit(image,(self.map_x + (col * self.CELL_WIDTH),self.map_y +(row * self.CELL_HEIGHT)))
    
    # Methode public update map before draw
    def update(self):
        pass

    # Methode public read sprite message to display
    def read_message(self,cell):
        if str(cell) in self.MAP_SPRITE:
            if "gui_message" in self.MAP_SPRITE[str(cell)]:
                return self.MAP_SPRITE[str(cell)]["gui_message"]
        return False

    # Methode private get image with is key 
    def __make_image(self,cell):          
        if str(cell) in self.MAP_SPRITE:
            sprite = self.MAP_SPRITE[str(cell)]['image']
            return pygame.image.load(sprite)
        return False
       

    # Methode private set items on map
    def __make_items(self):
        rand_values=[];
        for item in self.MAP_ITEMS:
            item_add = False
            while not item_add:
                row = randrange(0, self.MAP_ROW)
                col = randrange(0, self.MAP_COLUMN)
                cell = self.read_cell(row,col)
                if(cell == "0" and self.__can_draw_item(rand_values,row,col)):
                    self.make_cell(row,col,item)
                    rand_values.append((col,row))
                    item_add = True

    # Methode private difined if items can be draw
    def __can_draw_item(self,rand_values,row,col):
        can = True
        for val in rand_values:
            x,y = val
            if (x > col-self.ITEMS_SPACE and x < col+self.ITEMS_SPACE) or (y > row-self.ITEMS_SPACE and y < row+self.ITEMS_SPACE): 
                can = False
                break
        return can


    # Methode private loading sprite json file
    def __load_sprite(self):
        with open('sprites.json') as data_file:    
            self.MAP_SPRITE = json.load(data_file)

    # Property return hero spawn point
    @property
    def spawn_point(self):
        return (self.spawn_point_x,self.spawn_point_y)

    # Property return Map position
    @property
    def map_position(self):
        return (self.map_x,self.map_y)


class Hero:
    # Defined hero sprite
    SPRITE = "./assets/hero.png"
    SPRITE_WIDTH = 21 # Sprite Width
    SPRITE_HEIGHT = 21 # Sprite Height

    def __init__(self,name,spawn_position,map_position):
        self.name = name
        self.spawn_position = spawn_position
        print(spawn_position,map_position)
        self.x, self.y = spawn_position
        self.map_x,self.map_y = map_position
        self.image = pygame.image.load(self.SPRITE)

    # Methode public drawing the hero on map
    def draw(self,screen):        
        screen.blit(self.image,(self.map_x + (self.x * self.SPRITE_WIDTH),self.map_y + (self.y * self.SPRITE_HEIGHT)))  

    # Methode public update user status
    def update(self,x,y):        
        self.__move(x,y)

    # Methode private change user position
    def __move(self,x,y):
        self.x += x
        self.y += y



class GameController:

    # Settings variable
    SCREEN_WIDTH = 640 # Game screen width size
    SCREEN_HEIGHT = 480 # Game screen height size
    GAME_CLOSED = False # Game status
    GAME_SCREEN_NAME = "MacGyver Escape RoOm" # Game screen name
    GAME_SCREEN_BACKGROUND = (0,0,0) # Game screen background color
    
    def __init__(self):
        pygame.init() # Pygame initialization
        # Create a new window with size 640 x 480 "width x height"
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # Set screen name
        pygame.display.set_caption(self.GAME_SCREEN_NAME)

        # Game keypress action Horizontal x Vertical y
        # value -1 0 1 for x left not move right same for y up not move down

        self.move_x = 0
        self.move_y = 0
        self.map = Map(self.SCREEN_WIDTH,self.SCREEN_HEIGHT) # Instanciate Map
        self.hero = Hero("Mc Guyver",self.map.spawn_point,self.map.map_position)

    def game_start(self):
        # Loop execute game until game_closed are false
        while not self.GAME_CLOSED:            
            self.__gamepad()
            self.__update()
            self.screen.fill(self.GAME_SCREEN_BACKGROUND)
            self.__draw()
            # self.__draw_message()
            pygame.display.update() # Pygame windows refresh 

        self.__quit();    

    # Method private contains actions to do every frame
    def __update(self):
        self.map.update()
        self.hero.update(self.move_x,self.move_y)

    # Method private contain actions to do before display in screen
    def __draw(self):
        self.map.draw(self.screen)
        self.hero.draw(self.screen)

    # Method private display a message on screen 
    def __draw_message(self,message):
        pass

    # Method private for keyboard actions
    def __gamepad(self):
        # Reste move
        self.move_x = 0 
        self.move_y = 0 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clic on cross windows
                self.GAME_CLOSED = True # exit game         
            if event.type == pygame.KEYDOWN: # User clic a touch  
                if event.key == pygame.K_LEFT: # User clic left
                    self.move_x = -1
                elif event.key  == pygame.K_RIGHT: # User clic right
                    self.move_x = 1
                elif event.key  == pygame.K_UP: # User clic up
                    self.move_y = -1
                elif event.key  == pygame.K_DOWN: # User clic down
                    self.move_y = 1

    # Method private for leaved game
    def __quit(self):
        pygame.quit # close pygame
        quit() # close script

# instansiate game object 
game = GameController()
# Start game
game.game_start()






























