import pygame
import time

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
brown    = ( 150,  75,   0)
blue     = (   0,   0, 255)
yellow   = ( 255, 255,   0)
backcolor = (0x9F, 0xAF, 0xF8)
spaceblue = (0x1B, 0x1B, 0x9E)
editblue = (   0, 110, 173)

class Scout(object):
	def __init__(self, true_pos=(0,0), center=(0,0), id_num=0):
		self.center = center
		self.true_pos = true_pos

		pygame.init()
		self.image = pygame.image.load('scout_icon.png')
		#self.image = pygame.image.load('cuttlefish.png')
		self.width,self.height = self.image.get_size()
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)

		self.id_num = id_num

	def render(self,surface):
		surface.blit(self.image, self.top_left)
		surface.blit(((pygame.font.Font(None,35)).render(str(self.id_num),True,black)), (self.center[0]-6,self.center[1]-11))

class Waypoint(object):
	def __init__(self, true_pos=(0,0), center=(0,0), way_type=0, id_num=0, description='',owner=0):
		self.center = center
		self.true_pos = true_pos
		self.owner = owner

		self.description = description

		pygame.init()
		if way_type==3:
			self.image = pygame.image.load('waypoint_red.png')
		elif way_type==2:
			self.image = pygame.image.load('waypoint_blue.png')
		elif way_type==1:
			self.image = pygame.image.load('waypoint_green.png')
		else:
			self.image = pygame.image.load('waypoint_purple.png')

		self.width,self.height = self.image.get_size()
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)

		self.id_num = id_num

	def render(self,surface):
		surface.blit(self.image, self.top_left)
		surface.blit(((pygame.font.Font(None,35)).render(str(self.id_num),True,black)), (self.center[0]-6,self.center[1]-11))

class MapDataStruct(object):
	def __init__(self):
		self.chain_list = []
		self.waypoint_list = []
		self.scout_list = []

	def update(self,inputObj):
		scout_centers = {}
		waypoint_centers = {}
		chain_centers = {}

		for idNum in inputObj.scout_id_list:
			scout_centers[idNum] = self.coordinate_transform(inputObj.current_positions[idNum])
			for point in inputObj.positions_list[idNum]:

				if not (idNum in chain_centers):
					chain_centers[idNum] = [self.coordinate_transform(point)]
				else:
					chain_centers[idNum].append(self.coordinate_transform(point))		
		for idNum in inputObj.waypoint_ids:
			waypoint_centers[idNum] = self.coordinate_transform(inputObj.waypoint_positions[idNum])

		for idNum in inputObj.scout_id_list:
			if(inputObj.current_positions[idNum] in inputObj.positions_list[idNum]):
				scTemp = Scout(inputObj.current_positions[idNum],scout_centers[idNum],idNum)
				self.scout_list.append(scTemp)
			chTemp = Chain(chain_centers[idNum])
			self.chain_list.append(chTemp)
		for idNum in inputObj.waypoint_ids:
			wpTemp = Waypoint(inputObj.waypoint_positions[idNum], waypoint_centers[idNum], inputObj.waypoint_types[idNum], idNum, inputObj.waypoint_labels[idNum], inputObj.waypoint_owners[idNum])
			self.waypoint_list.append(wpTemp)


	def coordinate_transform(self,coords_In):
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
			pygame.draw.lines(surface,blue,False,self.points_list,7)
		for point_OP in self.points_list:
			pygame.draw.circle(surface,black,point_OP,6,0)

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
		self.map_base = pygame.image.load('kresge_map.png')

	def render(self):
		self.display.fill(yellow) #255,255,0 is Yellow!
		self.display.blit(self.map_base,(0,0))

		for chain in self.map_data.chain_list:
			chain.render(self.display)
		for waypoint in self.map_data.waypoint_list:
			waypoint.render(self.display)
		for scout in self.map_data.scout_list:
			scout.render(self.display)


		self.pg_disp.update()

	def pan_horizontal(self,delta_x):
		pass

	def pan_vertical(self, delta_y):
		pass

	def open_waypoint_menu(self):
		pass

	def close_waypoint_menu(self):
		pass