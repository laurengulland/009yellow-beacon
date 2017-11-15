import pygame
import time
import math

red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)
darkyellow = (200,200,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

scoutimg = pygame.image.load('scout_icon.png')

poi_img = pygame.image.load('waypoint_blue.png')

        
scoutx = 400
scouty = 100
scoutxpos = 200
scoutypos_init = 50

def text_objects(text,font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()



class Menu(object):
    def __init__(self):
        self.DISP_WIDTH = 600
        self.DISP_HEIGHT = 400

        self.scoutMenuBool = False
        
        pygame.init()
        self.pgdisp = pygame.display
        self.display = self.pgdisp.set_mode((self.DISP_WIDTH, self.DISP_HEIGHT))
        self.pgdisp.set_mode((self.DISP_WIDTH, self.DISP_HEIGHT))
        self.pgdisp.set_caption('Side Menu Test')
        self.clock = pygame.time.Clock()
#        FPS = 60'

    def scout(self,x,y):
        self.display.blit(scoutimg, (x,y))

    def poi(self,x,y):
        self.display.blit(poi_img,  (x,y))
    
    def menu_button(self, msg, x, y, width, height, inactive, active, action = None, buttontype = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        smalltext = pygame.font.Font('freesansbold.ttf',20)
        smallertext = pygame.font.Font('freesansbold.ttf',15)

        #Button highlight
                
        if x+width>mouse[0]>x and y+height>mouse[1]>y:
            pygame.draw.rect(self.display, active, (x,y,width,height), 0)
            pygame.draw.rect(self.display, black, (x,y,width,height), 5)
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
            pygame.draw.rect(self.display, inactive, (x,y,width,height), 0)
            pygame.draw.rect(self.display, black, (x,y,width,height), 5)

        #draw button border


        if buttontype == "main":
            textSurf, textRect = text_objects(msg, smalltext)
            textRect.center = ((x+width/2),y+height/2)
            self.display.blit(textSurf, textRect)
        if buttontype == "scout":
            textSurf, textRect = text_objects(msg, smallertext)
            textRect.center = ((x+width/2),y+15)
            self.display.blit(textSurf, textRect)
        if buttontype == None:
            None
    
        

    def arrow_button(self, rectx, recty, rectw, recth, vert1, vert2, vert3, inactive, active):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #draw button
        pygame.draw.rect(self.display,black,(rectx,recty,rectw,recth),0)
        pygame.draw.rect(self.display, black, (rectx,recty,rectw,recth), 5)

        #button highlight
        if rectx+rectw>mouse[0]>rectx and recty+recth>mouse[1]>recty:
            pygame.draw.polygon(self.display, active, [vert1,vert2,vert3], 0)
        else:
            pygame.draw.polygon(self.display, inactive, [vert1, vert2, vert3], 0)
                   
        
    def side_menu(self):
        self.display.fill(black)
        
        self.menu_button("     Scouts", scoutx, scoutypos_init, scoutxpos, scouty,darkyellow , yellow, "scoutlist", "main")
        self.scout(scoutx+40,scoutypos_init+27)
        self.menu_button("       POIs", scoutx, scoutypos_init+scouty, scoutxpos, scouty, darkyellow, yellow, "POIlist", "main")
        self.poi(scoutx+32,scoutypos_init+scouty+27)
        self.menu_button("Settings", scoutx, scoutypos_init+2*scouty, scoutxpos, scouty,darkyellow,yellow, "settings", "main")

        self.arrow_button(400, 0, 200, 50, [500, 10], [475, 40], [525, 40], darkyellow, yellow)#top
        self.arrow_button(400, 350, 200, 50, [500, 390], [475, 360], [525, 360], darkyellow, yellow)#bottom
                          
        self.pgdisp.update()
        self.clock.tick(15)

    def scoutlist(self):
        self.scoutMenuBool = True
        
        self.display.fill(black)
        
        self.menu_button("     Scout 1", scoutx, scoutypos_init, scoutxpos, scouty,darkyellow,yellow, None, "scout")
        self.scout(scoutx+40,scoutypos_init+27)
        self.menu_button("     Scout 2", scoutx, scoutypos_init+scouty, scoutxpos, scouty,darkyellow,yellow, None, "scout")
        self.scout(scoutx+40,scoutypos_init+scouty+27)
        self.menu_button("     Scout 3", scoutx, scoutypos_init+2*scouty, scoutxpos, scouty,darkyellow,yellow, None, "scout")
        self.scout(scoutx+40,scoutypos_init+2*scouty+27)
        
        self.arrow_button(400, 0, 200, 50, [500, 10], [475, 40], [525, 40], darkyellow, yellow)#top
        self.arrow_button(400, 350, 200, 50, [500, 390], [475, 360], [525, 360], darkyellow, yellow)#bottom
                          
        self.pgdisp.update()
        self.clock.tick(15)

    def POIlist():
        None
    def settings():
        None
        
    def run(self):
        crashed = False
        while not crashed:
            if self.scoutMenuBool:
                self.scoutlist()
            else:
                self.side_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                    
        pygame.quit()
        quit()


if __name__ == '__main__':
    gui = Menu()
    gui.run()
