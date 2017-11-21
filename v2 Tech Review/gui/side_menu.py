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

scoutimg = pygame.image.load('sprites/scout_icon.png')

poi_img = pygame.image.load('sprites/waypoint_blue.png')


scoutx = 400
scouty = 100
scoutxpos = 200
scoutypos_init = 50

def text_objects(text,font):
    print('TEXT OBJECTS EVALUATING')
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()



class Menu_GUI(object):
    def __init__(self, disp_width=600, disp_height=400):
        self.DISP_WIDTH = disp_width #should be passed in from controller, which reads screen dimensions from JSON file
        self.DISP_HEIGHT = disp_height #should be passed in from controller, which reads screen dimensions from JSON file
        self.scoutMenuBool = False
        self.crashed = False #switches True when pygame screen is closed, triggers program exit

        #Initializes pygame. will eventually be integrated with rest of VIEW GUI.
        pygame.init()
        self.pgdisp = pygame.display
        self.pgdisp.set_caption('Side Menu Test')
        self.display = self.pgdisp.set_mode((self.DISP_WIDTH, self.DISP_HEIGHT))
        self.clock = pygame.time.Clock()

        #set other relevant variables!
        self.inactive_button_color = DARKYELLOW
        self.active_button_color = YELLOW
#        FPS = 60'
        print('------INITIALIZED MENU CLASS')

    def display_scout(self,x,y):
        print('SCOUT EVALUATING')
        self.display.blit(scoutimg, (x,y))

    def display_poi(self,x,y):
        print('POI EVALUATING')
        self.display.blit(poi_img,  (x,y))

    def draw_menu_button(self, button_label, dimensions, action = None, buttontype = None):
        """message: label to put on button.
        dimensions: tuple of (top_left_x_coord, top_left_y_coord,width,height)
        action:
        buttontype:
        """
        print('MENU_BUTTON FUNCTION EVALUATING')
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        smalltext = pygame.font.Font('freesansbold.ttf',20)
        smallertext = pygame.font.Font('freesansbold.ttf',15)

        #Button highlight

        if x+width>mouse[0]>x and y+height>mouse[1]>y:
            pygame.draw.rect(self.display, self.active_button_color, dimensions, 0)
            pygame.draw.rect(self.display, BLACK, dimensions, 5)
            if click[0] == 1 and action != None:
                if buttontype == "main":
                    if action == "scoutlist":
                        self.scoutlist()
                    if action == "POIlist":
                        None
                    if action == "settings":
                        None
                if buttontype == "scout":
                    None
        else:
            pygame.draw.rect(self.display, self.inactive_button_color, (x,y,width,height), 0)
            pygame.draw.rect(self.display, BLACK, (x,y,width,height), 5)

        #draw button border


        if buttontype == "main":
            textSurf, textRect = text_objects(button_label, smalltext)
            textRect.center = ((x+width/2),y+height/2)
            self.display.blit(textSurf, textRect)
        elif buttontype == "scout":
            textSurf, textRect = text_objects(button_label, smallertext)
            textRect.center = ((x+width/2),y+15)
            self.display.blit(textSurf, textRect)
        elif buttontype == None:
            pass



    def arrow_button(self, rectx, recty, rectw, recth, vert1, vert2, vert3):
        print('ARROW_BUTTON FUNCTION EVALUATING')
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #draw button
        pygame.draw.rect(self.display,BLACK,(rectx,recty,rectw,recth),0)
        pygame.draw.rect(self.display, BLACK, (rectx,recty,rectw,recth), 5)

        #button highlight
        if rectx+rectw>mouse[0]>rectx and recty+recth>mouse[1]>recty:
            pygame.draw.polygon(self.display, self.active_button_color, [vert1,vert2,vert3], 0)
        else:
            pygame.draw.polygon(self.display, self.inactive_button_color, [vert1, vert2, vert3], 0)


    def side_menu(self):
        print('SIDE_MENU FUNCTION EVALUATING')
        self.display.fill(BLACK)
        # scoutx = 400
        # scouty = 100
        # scoutxpos = 200
        # scoutypos_init = 50
        self.draw_menu_button("     Scouts", scoutx, scoutypos_init, scoutxpos, scouty,DARKYELLOW , YELLOW, "scoutlist", "main")
        self.display_scout(scoutx+40,scoutypos_init+27)
        self.draw_menu_button("       POIs", scoutx, scoutypos_init+scouty, scoutxpos, scouty, DARKYELLOW, YELLOW, "POIlist", "main")
        self.display_poi(scoutx+32,scoutypos_init+scouty+27)
        self.draw_menu_button("Settings", scoutx, scoutypos_init+2*scouty, scoutxpos, scouty,DARKYELLOW,YELLOW, "settings", "main")

        self.arrow_button(400, 0, 200, 50, [500, 10], [475, 40], [525, 40], DARKYELLOW, YELLOW)#top
        self.arrow_button(400, 350, 200, 50, [500, 390], [475, 360], [525, 360], DARKYELLOW, YELLOW)#bottom

        self.pgdisp.update()
        self.clock.tick(15)

    def scoutlist(self):
        print('SCOUTLIST FUNCTION EVALUATING')
        self.scoutMenuBool = True

        self.display.fill(BLACK)

        self.draw_menu_button("     Scout 1", scoutx, scoutypos_init, scoutxpos, scouty,DARKYELLOW,YELLOW, None, "scout")
        self.display_scout(scoutx+40,scoutypos_init+27)
        self.draw_menu_button("     Scout 2", scoutx, scoutypos_init+scouty, scoutxpos, scouty,DARKYELLOW,YELLOW, None, "scout")
        self.display_scout(scoutx+40,scoutypos_init+scouty+27)
        self.draw_menu_button("     Scout 3", scoutx, scoutypos_init+2*scouty, scoutxpos, scouty,DARKYELLOW,YELLOW, None, "scout")
        self.display_scout(scoutx+40,scoutypos_init+2*scouty+27)

        self.arrow_button(400, 0, 200, 50, [500, 10], [475, 40], [525, 40], DARKYELLOW, YELLOW)#top
        self.arrow_button(400, 350, 200, 50, [500, 390], [475, 360], [525, 360], DARKYELLOW, YELLOW)#bottom

        self.pgdisp.update()
        self.clock.tick(15)

    def POIlist():
        print('--------------------POILIST EVALUATING')
        pass

    def settings():
        print('--------------------SETTINGS EVALUATING')
        pass

    def run(self):
        print('RUNNING')
        while not self.crashed:
            if self.scoutMenuBool:
                self.scoutlist()
            else:
                self.side_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
            time.sleep(.25)

        pygame.quit()
        quit()


if __name__ == '__main__':
    gui = Menu_GUI()
    gui.run()
