import serial
import io

CONST_HEADER = '<?xml version="1.0" encoding="UTF-8"?><gpx version="1.0">'
CONST_TAIL = '</gpx>'

class Point:
     def __init__(self, latitude, longitude, time, src, description=''):
         self.latitude = latitude
         self.longitude = longitude
         self.time = time
         self.description = description
         self.src = src

def toGPX (listWaypoints, listTracks):
	waypointFullString = ''
	for waypoint in listWaypoints:
		waypointString = '<wpt lat="' + waypoint.latitude + '" lon="' + waypoint.longitude + '">'
		waypointString += '<name>' + waypoint.description + '</name>'
		waypointString += '<src>' + waypoint.src + '</src>'
		waypointString += '</wpt>'
		waypointFullString += waypointString

	trackFullString = ''
	for track in listTracks:
		trackString = '<trk>'
		trackString += '<src>' + track[0].src + '</src>'
		if len(track[0].description) > 0:
			trackString += '<name>' + track[0].description + '</name>'
		trackString += '<trkseg>'
		for trackpoint in track:
			trackpointString = '<trkpt lat="' + trackpoint.latitude + '" lon="' + trackpoint.longitude + '">'
			trackpointString += '<time>'+ trackpoint.time +'</time>'
			trackpointString += '</trkpt>'
			trackString += trackpointString
		trackString += '</trkseg></trk>'
		trackFullString += trackString

	return CONST_HEADER + waypointFullString + trackFullString + CONST_TAIL

def parseGPS(GPSLine):
	line = GPSLine
	isPOI = True if int(line[0]) == 1 else False
	if isPOI:
		poi_id = line[1:3][::-1]
		latitude = hexCoordToString(line[3:8][::-1])
		longitude = hexCoordToString(line[8:13][::-1])
		scout_id = line[13]
		category = line[14]
		description = line[15:]

		waypoint = Point(latitude, longitude, 0, scout_id, description)
		listWaypoints.append(waypoint)
	else:
		for i in range(min(5, len(line)//15)): # int division
			start = i * 15
			latitude = hexCoordToString(line[start + 1 : start + 6][::-1])
			longitude = hexCoordToString(line[start + 6 : start + 11][::-1])
			scout_id = line[start + 11]
			timestamp = line[start + 12 : start + 16][::-1]

			trackpoint = Point(latitude, longitude, timestamp, scout_id, '')
			isFound = False
			for track in listTracks:
				if track[0].src == scout_id:
					track.append(trackpoint)
					isFound = True
			if not isFound:
				listTracks.append([trackpoint])
	
	GPSString = toGPX(listWaypoints, listTracks)
	writeToDisk(GPSString)
	return GPSString

def writeToDisk(GPSString):
	file = open("testfile.txt","w")
	file.write(GPSString)
	file.close()

def hexCoordToString(hexString):
	return str(float(hexString)/10.**6)



## Actual code that runs
# these lists keep track of all the points
listWaypoints = []
listTracks = []

# this code needs to be tested with serial inputs
# ser = serial.Serial('/dev/ttyUSB0', 9600)
while True:
 	inputHex = ser.read(80)
 	# inputHex = '31 32 32 33 34 35 36 37 38 39 30 31 32 33 34 64 65 73 63 72 69 70 74 69 6f 6e'
 	inputString = bytearray.fromhex(inputHex).decode()
 	parseGPS(inputString)

## Code to test the above functions
# inpString = '0 34567 89012 3 4444 00567 89012 3 4444 34567 89012 1 4444'.replace(' ', '')
# parseGPS(inpString) # 0 34567 89012 3 4444 0 00567 89012 3 4444 0 34567 89012 1 4444
# print parseGPS('122345678901234description') # 1 22 34567 89012 3 4 description




			
			      
