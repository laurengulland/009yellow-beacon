import pygame
import time

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREY     = ( 100, 100, 100)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BROWN    = ( 150,  75,   0)
BLUE     = (   0,   0, 255)
YELLOW   = ( 255, 255,   0)
BACKCOLOR = (0x9F, 0xAF, 0xF8)
SPACEBLUE = (0x1B, 0x1B, 0x9E)
EDITBLUE = (   0, 110, 173)
DARKYELLOW = (150,150,0)

class Scout(object):
	def __init__(self, true_pos=(0,0), center=(0,0), id_num=0):
		self.center = center
		self.true_pos = true_pos

		pygame.init()
		self.image = pygame.image.load('sprites/scout_icon.png')
		#self.image = pygame.image.load('cuttlefish.png')
		self.width,self.height = self.image.get_size()
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)

		self.id_num = id_num

	def render(self,surface):
		surface.blit(self.image, self.top_left)
		surface.blit(((pygame.font.Font(None,35)).render(str(self.id_num),True,BLACK)), (self.center[0]-6,self.center[1]-11))

class Waypoint(object):
	def __init__(self, true_pos=(0,0), center=(0,0), way_type=0, id_num=0, description='',owner=0):
		self.center = center
		self.true_pos = true_pos
		self.owner = owner
		self.way_type = way_type

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
		surface.blit(((pygame.font.Font(None,35)).render(str(self.id_num),True,BLACK)), (self.center[0]-6,self.center[1]-11))

class Waypoint_Highlighter(object):
	def __init__(self, center=(0,0)):
		self.center = center

		pygame.init()
		self.image = pygame.image.load('sprites/waypoint_selection_white.png')

		self.width,self.height = self.image.get_size()
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)

		self.exist = False

	def update(self,new_center,new_exist):
		self.center = new_center
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)
		self.exist = new_exist

	def render(self,surface):
		if self.exist:
			surface.blit(self.image, self.top_left)
		else:
			pass

class MapDataStruct(object):
	def __init__(self):
		self.chain_list = []
		self.waypoint_list = []
		self.scout_list = []

	def update(self,inputObj):
		self.chain_list = []
		self.waypoint_list = []
		self.scout_list = []
		scout_centers = {}
		waypoint_centers = {}
		chain_centers = {}

		for idNum in inputObj.scout_id_list:
			scout_centers[idNum] = self.coordinate_transform(inputObj.current_positions[idNum])
			if inputObj.positions_list[idNum] is None:
				continue
			for point in inputObj.positions_list[idNum]:
				if not (idNum in chain_centers):
					chain_centers[idNum] = [self.coordinate_transform(point)]
				else:
					chain_centers[idNum].append(self.coordinate_transform(point))
		for idNum in inputObj.waypoint_ids:
			waypoint_centers[idNum] = self.coordinate_transform(inputObj.waypoint_positions[idNum])

		for idNum in inputObj.scout_id_list:
			if inputObj.current_positions[idNum] is None or inputObj.positions_list[idNum] is None:
				continue
			if(inputObj.current_positions[idNum] in inputObj.positions_list[idNum]):
				scTemp = Scout(inputObj.current_positions[idNum],scout_centers[idNum],idNum)
				self.scout_list.append(scTemp)
			chTemp = Chain(chain_centers[idNum])
			self.chain_list.append(chTemp)
		for idNum in inputObj.waypoint_ids:
			wpTemp = Waypoint(inputObj.waypoint_positions[idNum], waypoint_centers[idNum], inputObj.waypoint_types[idNum], idNum, inputObj.waypoint_labels[idNum], inputObj.waypoint_owners[idNum])
			self.waypoint_list.append(wpTemp)


	def coordinate_transform(self,coords_In):
		#print('COORD TRANSFORM: coords_in =',coords_In,type(coords_In))
		bl_corner = (42.35804,-71.0950567)
		tr_corner = (42.35864,-71.0941733)
		frame_dim = (800,800)

		posOut = ( int(round((coords_In[1]-bl_corner[1])/(tr_corner[1]-bl_corner[1])*frame_dim[0])) , int(round((tr_corner[0]-coords_In[0])/(tr_corner[0]-bl_corner[0])*frame_dim[1])) )

		return posOut
		#return coords_In

class Chain(object):
	def __init__(self, points_list=[(0,0)]):
		self.points_list=points_list
		pygame.init()

	def render(self,surface):
		if len(self.points_list)>1:
			pygame.draw.lines(surface,BLUE,False,self.points_list,7)
		for point_OP in self.points_list:
			pygame.draw.circle(surface,BLACK,point_OP,6,0)

class Menu(object):
	def __init__(self,screen_width,screen_height,map_size):
		self.menu_coords = (map_size[0],0) #top left coordinates of menu are where map ends width-wise, and 0 for length-wise (top of screen = 0)
		self.menu_dimensions = (screen_width-map_size[0],screen_height)
		self.waypoint_render_indices = []

	def render(self,surface,map_data,selected_waypoint_index,is_menu_open):
		#dealing with only up to five waypoints currently, no scrolling features
		wp_count = 0
		button_dimensions = (int(self.menu_dimensions[0]*.8),int(self.menu_dimensions[1]*.15))
		if len(map_data.waypoint_list)==0: #if no waypoints, render a button saying so.
			#TEST ME, I'M UNTESTED!!
			button_coords_x = int(self.menu_dimensions[0]*.1)+self.menu_coords[0]
			button_coords_y = int(self.menu_dimensions[1]*.04)+self.menu_coords[1]
			Butttttton = Button((button_coords_x,button_coords_y), button_dimensions)#label="No POIs to display."
			Butttttton.render(surface)
		elif selected_waypoint_index==None: #if waypoint hasn't been selected, select the first one in the list.
			selected_waypoint_index = 0

		#SCROLLING FUNCTIONALITY. PLEASE SOMEONE REWRITE THIS IF YOU HAVE A BETTER WAY TO DO THIS.
		if len(self.waypoint_render_indices)!=len(map_data.waypoint_list): #if you got a dump of new waypoints or you
			if len(map_data.waypoint_list)>=5:
				print('EXPANDING WAYPOINT LIST (PAST FIVE)')
				if len(self.waypoint_render_indices)==0:
					start_idx = 0
				else:
					start_idx = self.waypoint_render_indices[0]
				self.waypoint_render_indices = list(range(len(map_data.waypoint_list)))[start_idx:start_idx+5]
			elif len(self.waypoint_render_indices)<6 and len(map_data.waypoint_list)<6:
				print('EXPANDING WAYPOINT LIST (UP TO FIVE)')
				self.waypoint_render_indices = list(range(len(map_data.waypoint_list)))
		if len(map_data.waypoint_list)>5 and len(self.waypoint_render_indices)>0:
			if selected_waypoint_index==self.waypoint_render_indices[-1]+1: #if there's a selected waypoint, make sure it's on screen.
				print('SCROLLING DOWN')
				self.waypoint_render_indices = list(range(len(map_data.waypoint_list)))[self.waypoint_render_indices[0]+1:self.waypoint_render_indices[0]+6]
			elif selected_waypoint_index==self.waypoint_render_indices[0]-1:
				print('SCROLLING UP')
				self.waypoint_render_indices = list(range(len(map_data.waypoint_list)))[self.waypoint_render_indices[0]-1:self.waypoint_render_indices[0]+4]
			if selected_waypoint_index not in self.waypoint_render_indices:
				if selected_waypoint_index<self.waypoint_render_indices[0]:
					print('SCROLLING ALL THE WAY TO TOP')
					self.waypoint_render_indices = list(range(len(map_data.waypoint_list)))[selected_waypoint_index:selected_waypoint_index+5]
				elif selected_waypoint_index>self.waypoint_render_indices[-1]:
					print('SCROLLING ALL THE WAY TO BOTTOM')
					self.waypoint_render_indices = list(range(len(map_data.waypoint_list)))[selected_waypoint_index-4:selected_waypoint_index+1]

		print(self.waypoint_render_indices)
		for index in self.waypoint_render_indices:
			waypoint = map_data.waypoint_list[index]
			button_coords_x = int(self.menu_dimensions[0]*.1)+self.menu_coords[0]
			button_coords_y = int(self.menu_dimensions[1]*.04)+self.menu_coords[1]+wp_count*(.04*self.menu_dimensions[1]+button_dimensions[1])
			Butttttton = Button((button_coords_x,button_coords_y), button_dimensions, wayObj=waypoint,active=(index==selected_waypoint_index and is_menu_open))
			if wp_count>=5: #stop after 5th waypoint, it won't fit on the screen anyway
				break
			Butttttton.render(surface)
			wp_count+=1
		return selected_waypoint_index
		#TO IMPLEMENT: consider adding arrows if some waypoints are off the screen!

class Button(object):
	def __init__(self,top_left,dimensions,wayObj=None,sprite_filepath="",active=False):
		"""top_left: tuple of (x,y) position denoting top_left corner
		dimensions: tuple of (width, height) of button
		"""
		self.active = active
		self.top_left_x, self.top_left_y = top_left
		self.width, self.height = dimensions
		if sprite_filepath != "":
			self.sprite = pygame.image.load(sprite_filepath)
		else:
			self.sprite = None
		self.inactive_color = GREY
		self.active_color = WHITE

		self.is_waypoint = not (wayObj is None)
		self.wayObj = wayObj

	def render(self,surface):
		#Draw Background Yellow Box
		#print(self.label,self.active)

		if self.active:
			pygame.draw.rect(surface, self.active_color, (self.top_left_x,self.top_left_y,self.width,self.height), 0)
		else:
			pygame.draw.rect(surface, self.inactive_color, (self.top_left_x,self.top_left_y,self.width,self.height), 0)
		#render sprite as icon for button
		if self.sprite is not None: #if there exists an icon for the button, draw it
			sprite_pos = (self.top_left_x+int(self.width/4-self.sprite.get_rect().size[0]/2),self.top_left_y+int(self.height/2-self.sprite.get_rect().size[1]/2)) #this needs to be calculated somewhere
			surface.blit(self.sprite,sprite_pos) #this needs to be display, not pg_display - not 100% sure how to pass in
		#Render Text for label
		if self.is_waypoint:
			self.render_text(surface,"POI #",(self.top_left_x+int(self.width/10),self.top_left_y+int(self.height/5)),fontsize=15)
			self.render_text(surface,str(self.wayObj.id_num),(self.top_left_x+int(self.width/10),self.top_left_y+int(1.1*self.height/2)),fontsize=60)
			self.render_text(surface,"Type "+str(self.wayObj.way_type)+" POI",(self.top_left_x+int(self.width/2),self.top_left_y+int(self.height/5)),fontsize=15)
			self.render_text(surface,str(self.wayObj.description),(self.top_left_x+int(self.width/2),self.top_left_y+int(self.height/5*2)),fontsize=15)
			self.render_text(surface,"Found by Scout #" + str(self.wayObj.owner),(self.top_left_x+int(self.width/2),self.top_left_y+int(self.height/5*3)),fontsize=15)
			self.render_text(surface,self.coord_builder(self.wayObj.true_pos),(self.top_left_x+int(self.width/2),self.top_left_y+int(self.height/5*4)),fontsize=15)
		else:
			self.render_text(surface,"No POIs to display.",(self.top_left_x+int(self.width/2),self.top_left_y+int(self.height/2)),fontsize=30)

	def coord_builder(self,coords):
		lati = coords[0]
		longi = coords[1]
		latMag = abs(lati)
		longMag = abs(longi)
		if lati > 0:
			nsLabel = "N"
		else:
			nsLabel = "S"
		if lati > 0:
			ewLabel = "E"
		else:
			ewLabel = "W"
		stringOut = str(latMag) + " N, " + str(longMag) + " W"
		return stringOut


	def render_text(self,surface,text,center_pos,fontsize=20):
		text_object = pygame.font.Font('freesansbold.ttf',fontsize)
		textSurface = text_object.render(text,True,BLACK)
		textRect = textSurface.get_rect()
		textRect.center = center_pos
		surface.blit(textSurface,textRect)

class GUI(object):
	def __init__(self, display_width=1200, display_height=800):
		self.display_width = display_width
		self.display_height = display_height

		self.map_data = MapDataStruct()

		#Initialize PyGame Display
		pygame.init()
		self.pg_disp = pygame.display
		self.display = self.pg_disp.set_mode((self.display_width,self.display_height))
		#self.display = self.pg_disp.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),flags=pygame.FULLSCREEN)
		self.pg_disp.set_caption('Beacon Technical Review GUI')
		self.map_base = pygame.image.load('sprites/kresge_map.png')
		self.Menu = Menu(self.display_width,self.display_height,self.map_base.get_rect().size)
		self.selected_waypoint_index = None

		self.gui_state = 'Menu'

		self.waypoint_hl = Waypoint_Highlighter()

	def render(self):
		self.display.fill(BLACK)
		self.display.blit(self.map_base,(0,0))

		for chain in self.map_data.chain_list:
			chain.render(self.display)
		for waypoint in self.map_data.waypoint_list:
			if (self.gui_state == 'Menu') and self.selected_waypoint_index is not None and (waypoint.id_num == self.map_data.waypoint_list[self.selected_waypoint_index].id_num):
				self.waypoint_hl.update(waypoint.center,True)
				self.waypoint_hl.render(self.display)
			waypoint.render(self.display)
		if not(self.gui_state == 'Menu'):
			self.waypoint_hl.update((0,0),False)
			self.waypoint_hl.render(self.display)

		for scout in self.map_data.scout_list:
			scout.render(self.display)

		if self.gui_state=='Menu':
			self.selected_waypoint_index = self.Menu.render(self.display,self.map_data,self.selected_waypoint_index,self.gui_state=='Menu')
		self.pg_disp.update()

	def move_left(self):
		print("__________LEFT__________")
		if self.gui_state == 'Menu':
			#navigate within the menu (probably doesn't mean anything)
			pass
		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		elif self.gui_state == 'Keyboard':
			#scroll through that keyboard son
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass
		self.render()

	def move_right(self):
		print("__________RIGHT__________")
		if self.gui_state == 'Menu':
			#navigate within the menu (probably doesn't mean anything)
			pass
		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		elif self.gui_state == 'Keyboard':
			#scroll through that keyboard son
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass
		self.render()

	def move_up(self):
		print("__________UP__________")
		if self.gui_state == 'Menu':
			#navigate within the menu
			if self.selected_waypoint_index!=None:
				self.selected_waypoint_index -= 1
			if self.selected_waypoint_index<0:
				self.selected_waypoint_index = len(self.map_data.waypoint_list)-1
		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		elif self.gui_state == 'Keyboard':
			#scroll through that keyboard son
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass
		self.render()

	def move_down(self):
		print("__________DOWN__________")
		if self.gui_state == 'Menu':
			#navigate within the menu
			if self.selected_waypoint_index!=None:
				self.selected_waypoint_index += 1
			if self.selected_waypoint_index>len(self.map_data.waypoint_list)-1:
				self.selected_waypoint_index = 0
		elif self.gui_state == 'Map':
			#pan left on the map (panning not implemented yet)
			pass
		elif self.gui_state == 'Keyboard':
			#scroll through that keyboard son
			pass
		else: #not a valid state!
			print('GUI_STATE NOT VALID.')
			pass
		self.render()

	def toggle_menu_state(self):
		#currently only toggles between Map and Menu, can add other states later
		if self.gui_state=='Map':
			self.gui_state='Menu'
		else:
			self.gui_state='Map'
		print('===================TOGGLING GUI STATE:',self.gui_state,'=================')
		self.render()
