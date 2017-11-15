import pygame
import time

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
brown    = ( 150,  75,   0)
blue     = (   0,   0, 255)
yellow   = ( 255, 255,   0)
YELLOW = (255,255,0)
DARKYELLOW = (200,200,0)
backcolor = (0x9F, 0xAF, 0xF8)
spaceblue = (0x1B, 0x1B, 0x9E)
editblue = (   0, 110, 173)

class Scout(object):
	def __init__(self, true_pos=(0,0), center=(0,0), id_num=0):
		self.center = center
		self.true_pos = true_pos

		pygame.init()
		self.image = pygame.image.load('sprites/scout_icon.png')
		#self.image = pygame.image.load('sprites/cuttlefish.png')
		self.width,self.height = self.image.get_size()
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)

		self.id_num = id_num

	def render(self,surface):
		surface.blit(self.image, self.top_left)
		surface.blit(((pygame.font.Font(None,35)).render(str(self.id_num),True,black)), (self.center[0]-6,self.center[1]-11))

class Waypoint(object):
	def __init__(self, true_pos=(0,0), center=(0,0), way_type=0, id_num=0, description=''):
		self.center = center
		self.true_pos = true_pos

		self.description = description

		pygame.init()
		if way_type==3:
			self.image = pygame.image.load('sprites/waypoint_red.png')
		elif way_type==2:
			self.image = pygame.image.load('sprites/waypoint_blue.png')
		elif way_type==1:
			self.image = pygame.image.load('sprites/waypoint_green.png')
		else:
			self.image = pygame.image.load('sprites/waypoint_purple.png')

		self.width,self.height = self.image.get_size()
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)

		self.id_num = id_num

	def render(self,surface):
		surface.blit(self.image, self.top_left)
		surface.blit(((pygame.font.Font(None,35)).render(str(self.id_num),True,black)), (self.center[0]-6,self.center[1]-11))

class Menu(object):
	def __init__(self):
		self.menu_state = 'POI_LIST' #will include other states in the future, currently implementing with just POI_LIST
		self.selected_poi = None
	def render(self,surface,map_data):
		#map_data.waypoint_list
		if self.menu_state == 'POI_LIST':
			if len(map_data.waypoint_list)==0: #if no POIS
				#render a button that says "no POIS" or something?
			else:
				#render all them POI buttons son
		#in the future, include other render states

class Button(object):
    def __init__(self,top_left,dimensions,label="",sprite=None):
        """top_left: tuple of (x,y) position denoting top_left corner
        dimensions: tuple of (width, height) of button
        """
        self.active = False
        self.top_left_x, self.top_left_y = top_left
        self.width, self.height = dimensions
        self.label = label
        self.sprite = sprite
        self.inactive_color = DARKYELLOW
        self.active_color = YELLOW

    def render(self,surface):
        if self.sprite:
            sprite_pos = (0,0) #this needs to be calculated somewhere
            surface.blit(sprite,sprite_pos) #this needs to be display, not pg_display - not 100% sure how to pass in
        #finish me!!


class MapDataStruct(object):
	def __init__(self):
		self.chain_list = []
		self.waypoint_list = []
		self.scout_list = []

	def update(self,testObj):
		pass

class Chain(object):
	def __init__(self, points_list=[(0,0)]):
		self.points_list=points_list
		pygame.init()

	def render(self,surface):
		if len(self.points_list)>1:
			pygame.draw.lines(surface,black,False,self.points_list,7)
		for point_OP in self.points_list:
			pygame.draw.circle(surface,black,point_OP,6,0)

class GUI(object):
	def __init__(self, display_width=1200, display_height=800):
		self.display_width = display_width
		self.display_height = display_height

		self.scout_list = []
		self.waypoint_list = []
		self.chain_list = []

		#Initialize PyGame Display
		pygame.init()
		self.pg_disp = pygame.display
		self.display = self.pg_disp.set_mode((self.display_width,self.display_height))
		#self.display = self.pg_disp.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),flags=pygame.FULLSCREEN)
		self.pg_disp.set_caption('Beacon Technical Review GUI')
		self.map_base = pygame.image.load('sprites/kresge_map.png')
		self.gui_state = 'Map' #state is one of 'Map', 'Menu', 'Keyboard' (not implemented yet), or ?

		self.Menu = Menu() #implement this!

	def render(self):
		self.display.fill(yellow)
		self.display.blit(self.map_base,(0,0))

		#render all the aspects of scouts and waypoints on top of the map
		for chain in self.chain_list:
			chain.render(self.display)
		for waypoint in self.waypoint_list:
			waypoint.render(self.display)
		for scout in self.scout_list:
			scout.render(self.display)

		#render the Menu of POIs
		if self.gui_state == 'Menu':
			self.menu.render(self.display,self.waypoint_list)
		# elif self.gui_state == 'Keyboard' #FOR THE FUTURE ANNOTATION ABILITY, NOT IMPLEMENTED YET
		# 	self.keyboard.render()
		# maybe move the above "MAP" rendering into this if block? But Menu/Keyboard should render on top of the map only, so not necessary.

		self.pg_disp.update()

	def move_left(self):
		if self.gui_state == 'Menu':
			#navigate within the menu (probably doesn't mean anything)
			pass
		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass

	def move_right(self):
		if self.gui_state == 'Menu':
			#navigate within the menu (probably doesn't mean anything)
			pass
		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass


	def move_up(self):
		if self.gui_state == 'Menu':
			#navigate within the menu
			self.menu.selected_poi -= 1

		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass

	def move_down(self):
		if self.gui_state == 'Menu':
			#navigate within the menu
			self.menu.selected_poi += 1
		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass

	def toggle_menu_state(self):
		if self.gui_state=='Map':
			self.gui_state=='Menu'
		else:
			self.gui_state=='Map'
