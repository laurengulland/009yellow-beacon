import time
import pygame
import mvp2_0_view as vw

class Data_to_Display(object):
#All positions are GPS positions, of the format (position_n, position_e), where position is a signed float.

	def __init__(self):
		scout_id_list = [1,2,3,4,5] #ids of Scouts.  List of unique integers identifying the Scouts.
		current_positions = [(200,200),(420,180),(500,250),(600,-100),(800,-100)] #list of most recent positions of the Scouts, corresponding to scout_id_list, regardless of whether they’re in range of the screen.
		positions_list = [[(200,200), (180,300), (210,600)],[(420,180),(400,300),(380,650)],[(550,500),(480,800)],[(600,100),(660,500)],[(800,-100),(820,300),(770,600)]] #list lists of positions of all scouts within frame, corresponds to the scout_id_list.
		waypoint_ids = [1,2] #ids of waypoints. List of unique integers identifying the waypoints.
		waypoint_types = [2,1] #type of waypoint, corresponding to waypoint_ids. If four buttons, each element will be an integer from one to four (inclusive)
		waypoint_labels = ['clothing','hazard'] #labels corresponding to the waypoint_ids. May be a list of empty strings if unlabeled.
		waypoint_positions = [(400,400), (600,600)] #positions of the waypoints, corresponds to waypoint_ids.
		waypoint_owners = [2,4]

class Tester(object):
	def __init__(self):
		self.gui = vw.GUI(1200,800)
		self.step_rate = 1 #for da loopy loop

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
				elif event.type == pygame.KEYDOWN: #currently reads up/down/left/right from keyboard, eventually switch this over to Queen Buttons, however those work
					self.gui.move_down()
				elif event.type == pygame.KEYUP:
					self.gui.move_up()
				elif event.type == pygame.KEYLEFT:
					self.gui.move_left()
				elif event.type == pygame.KEYRIGHT:
					self.gui.move_right()
					#HACK: Make right key temporarily actuate Map, should be changed once we have a dedicated Menu button
					self.gui.toggle_menu_state()
			time.sleep(self.step_rate)
			it+=1*self.step_rate
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
