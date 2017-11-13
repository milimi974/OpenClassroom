import pygame # Import Pygame Module

class Map:
    MAP_COLUMN = 15
    MAP_ROW = 15
    MAP_ITEMS = {"Une aiguille":"5","ether":"6","De l'éther":"7","Un petit tube en plastique":"8","Une clée":"9"}

    # Constructor
    def __init(self):
        # init map list
        self.level = [[0 for x in range(self.MAP_COLUMN)] for x in range(self.MAP_ROW)]

    # Methode public for create a new map
    def load_map(self,map):
        map_filename = "level_"+str(map)+".txt"
        with open(map_filename, "r") as f:            
            row = 0
            for line in f:
                line_list = ast.literal_eval(line)
                for cell in line_list:
                    column = line_list.index(cell)
                    self.level[row][column] = cell
                row += 1

    # Methode public change cell value
    def set_cell(self,row,column,item): 
        self.level[row][column] = item

    # Methode public check element on a position
    def get_cell(self,row,column):
        return self.level[row][column]
    # Methode private set items on map
    def __make_items(self):

   


class GameController:

    # Settings variable
    SCREEN_WIDTH = 640 # Game screen width size
    SCREEN_HEIGHT = 480 # Game screen height size
    GAME_CLOSED = False # Game status
    GAME_SCREEN_NAME = "MacGyver Escape RoOm" # Game screen name
    
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

    def game_start(self):
        # Loop execute game until game_closed are false
        while not self.GAME_CLOSED:            
            self.__gamepad()
            self.__upload()
            self.__draw()

        self.__quit();    

    # Method private contains actions to do every frame
    def __upload(self):
        pass

    # Method private contain actions to do before display in screen
    def __draw(self):
        pass

    # Method private for keyboard actions
    def __gamepad(self):
        # Reste move
        self.move_x = 0 
        self.move_y = 0 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clic on cross windows
                self.GAME_CLOSED = True # exit game            
            if event.type == pygame.K_LEFT: # User clic left
                self.move_x = -1
            if event.type == pygame.K_RIGHT: # User clic right
                self.move_x = 1
            if event.type == pygame.K_UP: # User clic up
                self.move_y = -1
            if event.type == pygame.K_DOWN: # User clic down
                self.move_y = 1

    # Method private for leaved game
    def __quit(self):
        pygame.quit # close pygame
        quit() # close script

# instansiate game object 
game = GameController()
# Start game
game.game_start()






























