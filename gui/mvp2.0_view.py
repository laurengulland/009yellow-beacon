import pygame

class GUI(object):
	def __init__(self):
		self.display_width = 600
		self.display_height = 400
		self.scout_list = []

		#Initialize PyGame Display
		pygame.init()
		self.pg_disp = pygame.display
		self.display = self.pg_disp.set_mode((self.display_width,self.display_height))
		self.pg_disp.set_caption('Cuttlefish GUI Test')
		self.cuttlefish = pygame.image.load('cuttlefish.jpg')

	def render(self):
		self.display.fill([255, 255, 0]) #255,255,0 is Yellow!
		self.display.blit(self.cuttlefish,(0,0))
		for scout in self.scout_list:
			self.display.blit(scout.image, scout.top_left)
		self.pg_disp.update()

	def pan_horizontal(self,delta_x):
		pass

	def pan_vertical(self, delta_y):
		pass

	def open_waypoint_menu(self):
		pass

	def close_waypoint_menu(self):
		pass


# if __name__ == '__main__':
	# gui = GUI_needs_better_name()
	# gui.run()
