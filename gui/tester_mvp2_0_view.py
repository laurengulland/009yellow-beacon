import time
import pygame
import mvp2_0_view as vw

class Tester(object):
	def __init__(self):
		self.gui = vw.GUI(1200,800)

	def run(self):
		crashed = False
		it = 0
		lineList = []
		while not crashed:
			#HACK addition of new scouts
			#after 2.5 seconds, add a scout. Normally this will be triggered by something else.
			if it<=5 and it%1==0:
				#self.add_scout(self.gui,(60*it,60*it),it)
				lineList.append((60*it,60*it))
				self.pos_scout(self.gui,(60*it,60*it),1)

			self.gui.chain_list = [vw.Chain(lineList)]
			self.gui.render()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True
			step_rate=1
			time.sleep(step_rate)
			it+=1*step_rate
			print(it)

		pygame.quit()
		quit()

	def pos_scout(self,gui_name,location,id_num): #To deprecate
		#new_scout = vw.Scout(location,id_num)
		new_scout = vw.Scout(location,id_num)
		gui_name.scout_list = [new_scout]

if __name__ == '__main__':
	gui_Tester = Tester()
	gui_Tester.run()