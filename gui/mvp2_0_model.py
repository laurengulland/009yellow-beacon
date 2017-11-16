import numpy as np
from tables import *

class LocationPoint(IsDescription):
	label = StringCol(16)     # 16-character String
	scout_id = Int64Col()
	time = Int64Col()
	gps_location_n = Float64Col()
	gps_location_e = Float64Col()
	is_point_of_interest = BoolCol()

class Data_to_Display(object): #object to be passed back in response to data_within_range().
	def __init__(self):
		self.scout_id_list = [] #ids of Scouts.  List of unique integers identifying the Scouts.
		self.current_positions = {} #list of most recent positions of the Scouts, corresponding to scout_id_list, regardless of whether they’re in range of the screen.
		self.positions_list = {} #list lists of positions of all scouts within frame, corresponds to the scout_id_list.
		self.waypoint_ids = [] #ids of waypoints. List of unique integers identifying the waypoints.
		self.waypoint_types = {} #type of waypoint, corresponding to waypoint_ids. If four buttons, each element will be an integer from one to four (inclusive)
		self.waypoint_labels = {} #labels corresponding to the waypoint_ids. May be a list of empty strings if unlabeled.
		self.waypoint_positions = {} #positions of the waypoints, corresponds to waypoint_ids.
		self.waypoint_owners = {} #
	#consider adding helper functions

	def add_scout_point(self,scout_id,location_tuple,is_current_position=False):
		location_n,location_e = location_tuple
		if scout_id not in scout_id_list:
			scout_id_list.append(scout_id)
		if is_current_position:
			current_positions = (location_n,location_e)
		if scout_id in positions_list:
			positions_list[scout_id] = positions_list[scout_id].append((location_n,location_e))
		else:
			positions_list[scout_id] = [(location_n,location_e)]

	def add_waypoint(self,waypoint_id,location_tuple,label,poi_type,scout_id):
		location_n,location_e=location_tuple
		waypoint_ids.append(waypoint_id)
		waypoint_labels[waypoint_id] = label
		waypoint_positions[waypoint_id] = (location_n,location_e)
		waypoint_types[waypoint_id] = poi_type
		waypoint_owners[waypoint_id] = scout_id

	# I (Karen) thinks it makes more sense to use dictionaries, so commented out list implementation
	# def add_scout_point(self,scout_id,location,is_current_position=False):
	#   if scout_id not in self.scout_id_list:
 #            self.scout_id_list.append(scout_id)
 #            self.current_positions.append(location)
 #            self.positions_list.append([location])
 #        else:
 #            index = self.scout_id_list.index(scout_id)
 #            if is_current_position:
 #                self.current_positions[index] = location
 #            self.positions_list[index].append(location)

	# def add_waypoint(self,waypoint_id,location,label):
 #        waypoint_ids.append(waypoint_id)
 #        waypoint_labels.append(label)
 #        waypoint_positions.append(location)

class Scouts(object):
	def __init__(self): #this should only be called once, as it will delete any previous file with this name
		self.filename = "modeltestfile.h5"
		self.data_display = Data_to_Display()

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

	def add_data_point(self,scout_id,time,gps_tuple,is_point_of_interest,poi_type=0):
		gps_location_n,gps_location_e=gps_tuple
		h5file = open_file(self.filename, mode="a", title="Test file")
		table = h5file.root.tracks.readout
		row = table.row
		# Fill the table with 10 particles
		row['label'] = 'LocationPoint: %6d' % (scout_id)
		row['scout_id'] = scout_id
		row['time'] = time
		row['gps_location_n'] = gps_location_n
		row['gps_location_e'] = gps_location_e
		row['is_point_of_interest'] = is_point_of_interest
		row.append()
		# Flush the buffers for table, close file
		table.flush()
		h5file.close()
		# update the data to display model
		if is_point_of_interest:
			waypoint_id = len(self.data_display.waypoint_positions.keys())
			label = "label for this waypoint"
			self.data_display.add_waypoint(waypoint_id, (gps_location_n,gps_location_e), label, poi_type, scout_id)
		else:
			self.data_display.add_scout_point(scout_id, (gps_location_n,gps_location_e), true)

	# condition = '(name == b"Particle:      5") | (name == b"Particle:      7")'
	def data_from_time(self,begin_time,last_time):
		data = self.helper_query('(time >= ' + str(begin_time) + ') & (time <= ' + str(last_time) + ')')
		return data

	def data_from_scout(self,scout_id):
		data = self.helper_query('scout_id == ' + str(scout_id))
		return data

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

	def helper_query(self,condition):
		h5file = open_file(self.filename, mode = "r")
		table = h5file.root.tracks.readout
		data = table.read_where(condition) # can also specify the columns you want here (condition, field='scout_id')
		h5file.close()
		return data     # returns a np ndarray


if __name__ == '__main__':
	scouts = Scouts()
	scouts.add_data_point(1,10,(45,45),False)
	scouts.print_data()
	scouts.add_data_point(2,12,(45,45),True)
	print('\n\n')
	scouts.print_data()
	print(scouts.data_from_scout(1))
	print(scouts.data_from_time(0, 100000))
