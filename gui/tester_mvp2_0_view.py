import time
import pygame
import mvp2_0_view as vw

"""THIS CODE CONTAINS FAKE SIMULATION DATA FOR TESTING THE VIEW CLASSES"""

class Data_to_Display(object):
#All positions are GPS positions, of the format (position_n, position_e), where position is a signed float.

	# def __init__(self):
	# 	self.scout_id_list = [1,2,3,4,5] #ids of Scouts.  List of unique integers identifying the Scouts.
	# 	self.current_positions = {1:(200,200),2:(420,180),3:(500,250),4:(600,-100),5:(800,-100)} #list of most recent positions of the Scouts, corresponding to scout_id_list, regardless of whether they’re in range of the screen.
	# 	self.positions_list = {1:[(200,200), (180,300), (210,600)], 2:[(420,180),(400,300),(380,650)], 3:[(550,500),(480,800)], 4:[(600,100),(660,500)], 5:[(800,-100),(820,300),(770,600)]} #list lists of positions of all scouts within frame, corresponds to the scout_id_list. 
	# 	self.waypoint_ids = [1,2] #ids of waypoints. List of unique integers identifying the waypoints.
	# 	self.waypoint_types = {1:2,2:1} #type of waypoint, corresponding to waypoint_ids. If four buttons, each element will be an integer from one to four (inclusive)
	# 	self.waypoint_labels = {1:'clothing', 2:'hazard'} #labels corresponding to the waypoint_ids. May be a list of empty strings if unlabeled.
	# 	self.waypoint_positions = {1:(400,400), 2:(600,600)} #positions of the waypoints, corresponds to waypoint_ids.
	# 	self.waypoint_owners = {1:2,1:4}

	def __init__(self):
		self.scout_id_list = [1] #ids of Scouts.  List of unique integers identifying the Scouts.
		self.current_positions = {1:(200,200)} #list of most recent positions of the Scouts, corresponding to scout_id_list, regardless of whether they’re in range of the screen.
		self.positions_list = {1:[(200,200), (180,300), (210,600)]} #list lists of positions of all scouts within frame, corresponds to the scout_id_list. 
		self.waypoint_ids = [1] #ids of waypoints. List of unique integers identifying the waypoints.
		self.waypoint_types = {1:2} #type of waypoint, corresponding to waypoint_ids. If four buttons, each element will be an integer from one to four (inclusive)
		self.waypoint_labels = {1:'clothing'} #labels corresponding to the waypoint_ids. May be a list of empty strings if unlabeled.
		self.waypoint_positions = {1:(400,400)} #positions of the waypoints, corresponds to waypoint_ids.
		self.waypoint_owners = {1:1}

class Tester(object):
	def __init__(self):
		self.gui = vw.GUI(1200,800)
		self.dtd = Data_to_Display()

	def run(self):
		crashed = False
		it = 0
		lineList = []
		while not crashed:
			#HACK addition of new scouts
			#after 2.5 seconds, add a scout. Normally this will be triggered by something else.
			# if it<=5 and it%1==0:
			# 	#self.add_scout(self.gui,(60*it,60*it),it)
			# 	lineList.append((60*it,60*it))
			# 	self.pos_scout(self.gui,(60*it,60*it),1)

			# self.gui.chain_list = [vw.Chain(lineList)]

			self.gui.map_data.update(self.dtd)
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