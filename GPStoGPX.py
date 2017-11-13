# listWaypoints: [point]
# listTracks: [[point, point]]
CONST_HEADER = '<?xml version="1.0" encoding="UTF-8"?><gpx version="1.0">'
CONST_TAIL = '</gpx>'

class Point:
     def __init__(self, latitude, longitude, time, name='', src=''):
         self.latitude = latitude
         self.longitude = longitude
         self.time = time
         self.name = name
         self.src = src

def toGPX (listWaypoints, listTracks):
	waypointFullString = ''
	for waypoint in listWaypoints:
		waypointString = '<wpt lat="' + waypoint.latitude + '" lon="' + waypoint.longitude + '">'
		waypointString += '<name>' + waypoint.name + '</name>'
		waypointString += '</wpt>'
		waypointFullString += waypointString

	trackFullString = ''
	for track in listTracks:
		trackString = '<trk>'
		trackString += '<src>' + track[0].src + '</src>'
		if len(track[0].name) > 0:
			trackString += '<name>' + track[0].name + '</name>'
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
	listWaypoints = []
	listTracks = []
	listArg = GPSLine.split()
	latitude = listArg[0]
	longitude = listArg[1]
	time = listArg[2]
	name = listArg[3]
	src = listArg[4]

	waypoint = Point(latitude, longitude, time, name, src)
	trackpoint = [Point(latitude, longitude, time, name, src)]
	listWaypoints.append(waypoint)
	listTracks.append(trackpoint)
	return toGPX(listWaypoints, listTracks)

print parseGPS('12 34 12:00 test Karen')


			
			      
