"""
For Software Architecture description:
	see Yellow 2.009 Google Drive > Tech Review > Electronics Design > Queen Software > Queen Software Architecture
"""

import pandas as pd
import numpy as np
import time
import json
import serial
import model

class Controller(object):
	def __init__(self, device):
		#initialize serial communication
		self.port = serial.Serial('COM9') #MUST SELECT CORRECT PORT ON TABLE
		self.type = device
		self.id = str(0) #necessary for queen
		self.model = model.Model()

	def is_queen(self):
		return self.type == 'Queen'

	def is_hive(self):
		return self.type == 'Hive'

	def parse_inputs(self):
		'''
		decide correct course of action
		'''
		#Parse input and decide whether GPS or button is most accurate
		packet = self.port.read(83)
		length = packet[1]
		packtype = packet[2]
		content = bytearray(packet[3:2+length])
		if packtype == 0x00:
			self.parse_scout_input(content)
		if packtype == 0x01:
			self.parse_queen_input(content)
		if packtype == 0x02:
			self.transmit_data()
		if packtype == 0x03:
			self.store_data(content, length)

	def store_data(self, content, length):
		if content[0]==0x00:
			self.store_location_data(content, length//15)
		else:
			self.store_poi_data(content)

	def store_location_data(self, content, num_points):
		queen_id = content[1]
		for i in range(num_points):
			pointbytes = content[2+15*i:17+15*i]
			lat = self.get_signed_coord(pointbytes[0:5])
			lon = self.get_signed_coord(pointbytes[5:10])
			scout_id = pointbytes[10]
			loc_time = self.get_time_from_bytes(pointbytes[11:])
			if scout_id == 0xFF:
				self.model.add_hive_data_point(None,str(queen_id),False,False, lat, lon, None, loc_time)
			else:
				self.model.add_hive_data_point(str(scout_id),None,False,False,lat,lon,None,loc_time)

	def store_poi_data(self, content):
		queen_id = content[1]
		lat = self.get_signed_coord(content[2:7])
		lon = self.get_signed_coord(content[7:12])
		scout_id = content[12]
		description = str(content[13:], 'ascii')
		if scout_id == 0xFF:
			self.model.add_hive_data_point(None,str(queen_id),True,False,lat,lon,description,None)
		else:
			self.model.add_hive_data_point(str(scout_id),None,True,False,lat,lon,description,None)

	def parse_scout_input(self, content):
		'''
		parses payload of gps input
		'''
		slat = self.get_signed_coord(content[0:5])
		slon = self.get_signed_coord(content[5:10])
		scout_id = content[11]
		scout_time = self.get_time_from_bytes(content[12:16])
		self.model.add_location_data_point(str(scout_id),None,slat,slon,scout_time)
		is_stale = content[16] == 1
		has_poi = content[17]==1
		if has_poi:
			plat = self.get_signed_coord(content[18:23])
			plon = self.get_signed_coord(content[23:28])
			#scout_id = content[28] this is redundant
			poi_time = self.get_time_from_bytes(content[29:33])
			self.model.add_poi_data_point(str(scout_id),None,plat,plon,poi_time,None)

	def parse_queen_input(self, content):
		'''
		parses payload of gps input
		'''
		qlat = self.get_signed_coord(content[0:5])
		qlon = self.get_signed_coord(content[5:10])
		queen_id = content[11]
		queen_time = self.get_time_from_bytes(content[12:16])
		self.model.add_location_data_point(None,str(queen_id),qlat,qlon,queen_time, None)

	def transmit_data(self, content):
		packet = self.location_data_packet()
		if packet is None:
			packet = self.poi_data_packet()
		if packet is None:
			packet = bytearray(83)
			packet[0]=0x7e
			packet[1]=1
			packet[2]=0x03
		self.port.write(packet)

	def location_data_packet(self):
		data = self.model.location_data_to_send()
		if data ==[]:
			return None
		packet = bytearray(83)
		packet[0]=0x7e
		packet[1]=3
		packet[2]=0x03
		packet[3]=0x00
		packet[4]=int(self.id)
		for i in range(len(data)):
			point = data[i]
			packet[5+i*15 : 20+i*15] = self.get_packet_data(point)
			packet[1] = packet[1]+15
		return packet

	def poi_data_packet(self):
		data = self.model.poi_data_to_send()
		if data is None:
			return None
		packet = bytearray(83)
		packet[0] = 0x7e
		descbytes = bytearray(data['description'],'ascii')
		packet[1]=13+len(descbytes)
		packet[2]=0x03
		packet[3]=0x01
		packet[4]=int(self.id)
		packet[5:10]=self.get_coord_bytes(data['latitude'])
		packet[10:15] = self.get_coord_bytes(data['longitude'])
		packet[15]=int(data['scout'])
		for i in range(len(descbytes)):
			packet[16+i] = descbytes[i]
		return packet

	def get_packet_data(self,point):
		lat = point['latitude']
		lon = point['longitude']
		scout_id = point['scout']
		timestamp = point['time']
		if scout_id is None:
			scout_id = 0xFF
		return self.get_coord_bytes(latitude)+self.get_coord_bytes(longitude)+bytearray([int(scout_id)])+self.time_int_to_bytearray(timestamp)

	def get_time_from_bytes(self, timebytes):
		return timebytes[0]+timebytes[1]*256+timebytes[2]*256^2+timebytes[3]*256^3

	def time_int_to_bytearray(self,timeint):
		'''
		helper function to convert integer seconds from epoch to hex.
		uses same least-significant-first convention as lat/long
		'''
		return bytearray([
			   timeint % 256,
			   (timeint // 256) % 256,
			   (timeint // (256**2)) % 256,
			   (timeint // (256**3)) % 256
			   ])

	def get_signed_coord(self, coord_bytes):
		'''
		helper function to convert coordinate bytes to numbers
		'''
		return (coord_bytes[0]+coord_bytes[1]*256+coord_bytes[2]*256**2+coord_bytes[3]*256**3)*(-1)**(coord_bytes[4]-1) *10**(-6)

	def get_coord_bytes(self, coord_float):
		if coord_float < 0:
			sign = 0x02
		else:
			sign = 0x01
		coordint = abs(coord_float*(10**6))
		return bytearray([
			coordint % 256,
			(coordint // 256) % 256,
			(coordint // 256**2) % 256,
			(coordint // 256**3) % 256,
			sign
		])

	def run(self):
		while True:
			self.parse_inputs()

if __name__ == '__main__':
	controller = Controller()
	controller.run()
