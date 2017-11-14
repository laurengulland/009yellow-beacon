import numpy as np
from tables import *

class LocationPoint(IsDescription):
	label = StringCol(16)     # 16-character String
	scout_id = Int64Col()
	time = Int64Col()
	gps_location = Float64Col()
	is_point_of_interest = BoolCol()

class Data_to_Display(object): #object to be passed back in response to data_within_range().
	def __init__(self):
		self.scout_id_list = [] #ids of Scouts.  List of unique integers identifying the Scouts.
		self.current_positions = [] #list of most recent positions of the Scouts, corresponding to scout_id_list, regardless of whether they’re in range of the screen.
		self.positions_list = [] #list lists of positions of all scouts within frame, corresponds to the scout_id_list.
		self.waypoint_ids = [] #ids of waypoints. List of unique integers identifying the waypoints.
		self.waypoint_types = [] #type of waypoint, corresponding to waypoint_ids. If four buttons, each element will be an integer from one to four (inclusive)
		self.waypoint_labels = [] #labels corresponding to the waypoint_ids. May be a list of empty strings if unlabeled.
		self.waypoint_positions = [] #positions of the waypoints, corresponds to waypoint_ids.
	#consider adding helper functions
	def add_point(self,scout_id,location,is_current_position=False):
		if scout_id in self.scout_id_list:
			index = self.scout_id_list.index(scout_id)
		else:
			index = 0
		pass

class Scouts(object):
	def __init__(self):
		self.filename = "modeltestfile.h5"

		print("Creating file:", self.filename)
		# Open a file in "w"rite mode
		h5file = open_file(self.filename, mode="w", title="Test file")
		#create a tracks group
		tracks_group = h5file.create_group("/", 'tracks', 'Scout Tracks')
		print("Group '/tracks' created")
		# Create one table on tracks group
		table = h5file.create_table(tracks_group, 'readout', LocationPoint, "Readout example")
		print("Table '/tracks/readout' created")
		#instantiate empty dataframe
		#create file saving or whatever
		table.flush()
		h5file.close()

	def add_data_point(self,scout_id,time,gps_location,is_point_of_interest):

		h5file = open_file(self.filename, mode="w", title="Test file")
		table = h5file.root.tracks.readout
		row = table.row
		# Fill the table with 10 particles
		row['label'] = 'LocationPoint: %6d' % (scout_id)
		row['scout_id'] = scout_id
		row['time'] = time
		row['gps_location'] = gps_location
		row['is_point_of_interest'] = is_point_of_interest
		row.append()
		# Flush the buffers for table, close file
		table.flush()
		h5file.close()

	# condition = '(name == b"Particle:      5") | (name == b"Particle:      7")'
	def data_from_time(self,begin_time,last_time):
		# names = [ x['name'] for x in table.where("""(TDCcount > 3) & (20 <= pressure) & (pressure < 50)""") ]
		pass

	def data_from_scout(self,scout_id):
		pass

	def current_locations(self,number_of_scouts):
		pass

	def data_within_range(self,top_left_position,bottom_right_position):
		pass

	def print_data(self):
		h5file = open_file(self.filename, mode = "r")
		table = h5file.root.tracks.readout
		print('Table object:',table)
		print('Number of rows:',table.nrows)
		print('Table variable names with their type and shape:')
		print(repr(table))
		for row in table.where('scout_id>0'):
			print(row['scout_id'])
		# for name in table.colnames:
		#     print(name, ':= %s, %s' % (table.colnames[name], table.colnames[name].shape))
		print('end pretty print')
		h5file.close()


if __name__ == '__main__':
	scouts = Scouts()
	scouts.add_data_point(1,10,2000,False)
	scouts.print_data()
	scouts.add_data_point(2,12,12000,True)
	print('\n\n')
	scouts.print_data()
