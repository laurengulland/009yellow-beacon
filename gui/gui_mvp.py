import pygame
import time


class Scout(object):
	def __init__(self, center=(0,0)):
		self.center = center

		pygame.init()
		self.image = pygame.image.load('illuminati_icon.png')
		self.width,self.height = self.image.get_size()
		self.top_left = (self.center[0]-self.width/2,self.center[1]-self.height/2)



class GUI_needs_better_name(object):
	def __init__(self):
		self.display_width = 600
		self.display_height = 400
		self.scout_list = []

		#Initialize PyGame Display
		pygame.init()
		self.pg_disp = pygame.display
		self.display = self.pg_disp.set_mode((self.display_width,self.display_height))
 #       self.surface = self.pg_disp.getsurface()
		self.pg_disp.set_caption('Cuttlefish GUI Test')
		self.cuttlefish = pygame.image.load('cuttlefish.jpg')

	def draw_screen(self):
		self.display.fill([255, 255, 0]) #255,255,0 is Yellow!
		self.display.blit(self.cuttlefish,(0,0))
		for scout in self.scout_list:
			self.display.blit(scout.image, scout.top_left)
		self.pg_disp.update()

	def add_scout(self,location):
		new_scout = Scout(location)
		self.scout_list.append(new_scout)

	def run(self):
		crashed = False
		it = 0.0
		while not crashed:

			#HACK addition of new scouts
			#after 2.5 seconds, add a scout. Normally this will be triggered by something else.
			if it<=5 and it%1==0:
				self.add_scout((60*it,60*it))

			self.draw_screen()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True
			step_rate=0.25
			time.sleep(step_rate)
			it+=1*step_rate
			print(it)

		pygame.quit()
		quit()

if __name__ == '__main__':
	gui = GUI_needs_better_name()
	gui.run()
