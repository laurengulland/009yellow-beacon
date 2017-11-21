import pygame
import time
import math

#color constants
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
DARKYELLOW = (200,200,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,200,200)

class Menu_GUI(object):
    def __init__(self,disp_width=600,disp_height=400):
        self.DISP_WIDTH = disp_width #should be passed in from controller, which reads screen dimensions from JSON file
        self.DISP_HEIGHT = disp_height #should be passed in from controller, which reads screen dimensions from JSON file

        self.crashed = False #switches True when pygame screen is closed, triggers program exit
        self.wait_time = .25 #number of seconds to sleep between loops

        #Initializes pygame. will eventually be integrated with rest of VIEW GUI.
        pygame.init()
        self.pgdisp = pygame.display
        self.pgdisp.set_caption('Side Menu Test')
        self.display = self.pgdisp.set_mode((self.DISP_WIDTH, self.DISP_HEIGHT))
        self.clock = pygame.time.Clock()

        #set other relevant variables!
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()

        self.SettingsButton = Button() #need to properly initialize these all
        self.POIBUtton = Button()
        self.SettingsButton = Button()
        self.buttons = [ScoutsButton, POIButton, SettingsButton]

    def render_scouts(self):
        pass

    def render_menu(self):
        pass

    # def update_mouse_position(self):
    #     self.mouse = pygame.mouse.get_pos()
    #     self.click = pygame.mouse.get_pressed()

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass

    def run(self):
        while not self.crashed:
            self.update_mouse_position()
            if self.display_scoutlist:
                self.render_scouts()
            else:
                self.render_menu()
            for event in pygame.even.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                elif event.type == pygame.KEYDOWN:
                    self.move_down()
                elif event.type == pygame.KEYUP:
                    self.move_up()
                elif event.type == pygame.KEYLEFT:
                    self.move_left()
                elif event.type == pygame.KEYRIGHT:
                    self.move_right()
            time.sleep(self.wait_time)
        pygame.quit()
        quit()


class Button(object):
    def __init__(self,pygame_display,top_left,dimensions,label="",sprite=None):
        """top_left: tuple of (x,y) position denoting top_left corner
        dimensions: tuple of (width, height) of button
        """
        self.active = False
        self.pg_display = pygame_display
        self.top_left_x, self.top_left_y = top_left
        self.width, self.height = dimensions
        self.label = label
        self.sprite = sprite
        self.inactive_color = DARKYELLOW
        self.active_color = YELLOW

    def render(self):
        if self.sprite:
            sprite_pos = (0,0) #this needs to be calculated somewhere
            self.pg_display.blit(sprite,sprite_pos) #this needs to be display, not pg_display - not 100% sure how to pass in
        #finish me!!

    def press_action(self): #necessary??
        pass

#don't think this class is necessary
# class RectangularButton(Button):
#     def __init__(self,top_left,dimensions,label=""sprite=None):
#         Button.__init__(self,top_left,dimensions,label,sprite)
#         self.sprite = sprite
