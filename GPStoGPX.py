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
    while line[-1] == '0':
        line = line[0:-1]
    isPOI = True if int(line[0:2]) == 1 else False
    if isPOI:
        while len(line)<30:
            line = line + '0'
        poi_id = line[1:3][::-1]
        latitude = hexCoordToString(line[6:16])
        longitude = hexCoordToString(line[16:26])
        scout_id = line[26:28]
        category = line[28:30]
        description = line[31:]
        waypoint = Point(latitude, longitude, 0, scout_id, description)
        listWaypoints.append(waypoint)
    else:
        while len(line)%30 !=2:
            line = line + '0'
        for i in range(min(5, len(line)//30)): # int division
            start = i * 30
            latitude = hexCoordToString(line[start + 2 : start + 12])
            longitude = hexCoordToString(line[start + 12 : start + 22])
            scout_id = line[start + 22:start+24]
            timestamp = str(timeHexToInt(line[start + 24 : start + 32]))

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
    file = open("testfile.gpx","w")
    file.write(GPSString)
    file.close()

def hexCoordToString(hexString):
    hexarray = []
    for i in range(5):
        hexarray.append(hexString[2*i:2*i+2])
    numarray = hexarray[0:4][::-1]
    numstring = ''.join(numarray[0:4])
    output = int(numstring,16)
    output = float(output)/(10**6)
    if hexarray[-1]=='02':
        output = -output
    return str(output)

def timeHexToInt(hexstring):
    return int(''.join([
        hexstring[6:8],
        hexstring[4:6],
        hexstring[2:4],
        hexstring[0:2]
    ]),16)


## Actual code that runs
# these lists keep track of all the points
listWaypoints = []
listTracks = []

# this below serial code needs to be tested with serial inputs
ser = serial.Serial('COM4', 9600)
while True:
    readin = ser.read(80)
    #the above serial code needs to be tested

    inputString = bytearray(readin).hex()
    printString = parseGPS(inputString)
    print(printString)
## Code to test the above functions
# inpString = '0 34567 89012 3 4444 00567 89012 3 4444 34567 89012 1 4444'.replace(' ', '')
# parseGPS(inpString) # 0 34567 89012 3 4444 0 00567 89012 3 4444 0 34567 89012 1 4444
# print parseGPS('122345678901234description') # 1 22 34567 89012 3 4 description
# inputHex = '31 32 32 33 34 35 36 37 38 39 30 31 32 33 34 64 65 73 63 72 69 70 74 69 6f 6e'
