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
	def __init__(self):
		#initialize serial communication
		self.port = serial.Serial('COM10') #MUST SELECT CORRECT PORT ON TABLE
		self.id = str(0) #necessary for queen
		self.model = model.Model()

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

	def parse_scout_input(self, content):
		'''
		parses payload of gps input
		'''
		slat = self.get_signed_coord(content[0:5])
		slon = self.get_signed_coord(content[5:10])
		scout_id = content[10]
		scout_time = self.get_time_from_bytes(content[11:15])
		self.model.add_location_data_point(str(scout_id),None,slat,slon,scout_time)
		is_stale = content[15] == 1
		has_poi = content[16]==1
		if has_poi:
			plat = self.get_signed_coord(content[17:22])
			plon = self.get_signed_coord(content[22:27])
			#scout_id = content[27] this is redundant
			poi_time = self.get_time_from_bytes(content[28:32])
			self.model.add_poi_data_point(str(scout_id),str(self.id),plat,plon,poi_time,None)

	def parse_queen_input(self, content):
		'''
		parses payload of gps input
		'''
		qlat = self.get_signed_coord(content[0:5])
		qlon = self.get_signed_coord(content[5:10])
		queen_id = content[11]
		queen_time = self.get_time_from_bytes(content[12:16])
		self.model.add_location_data_point(None,str(queen_id),qlat,qlon,queen_time, None)

	def transmit_data(self):
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
		if data is None:
			return None
		packet = bytearray(83)
		packet[0]=0x7e
		packet[1]=19
		packet[2]=0x03
		packet[3]=0x00
		packet[4:21] = self.get_packet_data(data)
		return packet

	def poi_data_packet(self):
		data = self.model.poi_data_to_send()
		if data is None:
			return None
		packet = bytearray(83)
		packet[0] = 0x7e
		if data['description'] is not None:
			descbytes = bytearray(data['description'],'ascii')
		else:
			descbytes = bytearray()
		packet[1]=14+len(descbytes)
		packet[2]=0x03
		packet[3]=0x01
		queen = data['queen']
		if queen is None:
			packet[4] = 0xFF
		else:
			packet[4]=int(queen)
		packet[5:10]=self.get_coord_bytes(data['latitude'])
		packet[10:15] = self.get_coord_bytes(data['longitude'])
		scout = data['scout']
		if scout is None:
			packet[15]=0xFF
		else:
			packet[15]=int(scout)
		timestamp = data['time']
		packet[16:20] = self.time_int_to_bytearray(timestamp)
		for i in range(len(descbytes)):
			packet[21+i] = descbytes[i]
		return packet

	def get_packet_data(self,point):
		lat = point['latitude']
		lon = point['longitude']
		scout_id = point['scout']
		queen_id = point['queen']
		timestamp = point['time']
		current = point['isCurrent']
		if current:
			cbyte = 1
		else:
			cbyte = 0
		if scout_id is None:
			scout_id = 0xFF
		if queen_id is None:
			queen_id = 0xFF
		return bytearray([int(queen_id)])+self.get_coord_bytes(lat)+self.get_coord_bytes(lon)+bytearray([int(scout_id)])+self.time_int_to_bytearray(timestamp)+bytearray([cbyte])

	def get_time_from_bytes(self, timebytes):
		return timebytes[0]+timebytes[1]*256+timebytes[2]*256**2+timebytes[3]*256**3

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
			sign = 2
		else:
			sign = 1
		coordint = int(abs(coord_float*(10**6)))
		return bytearray([
			coordint % 256,
			(coordint // 256) % 256,
			(coordint // 256**2) % 256,
			(coordint // 256**3) % 256,
			sign
		])

	def run(self):
		for i in range(10):
			print(i)
			self.parse_inputs()

if __name__ == '__main__':
	controller = Controller()
	controller.run()
