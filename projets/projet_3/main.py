import pygame # Import Pygame Module

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
        if(self.move_x != 0):
            print(self.move_x)
        if(self.move_y != 0):
            print(self.move_y)

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






























