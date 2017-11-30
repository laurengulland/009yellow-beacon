import pymongo

class DataPoint(object):
    def __init__(self, scout, queen, is_poi, is_current, latitude, longitude, description, time, needs_transmit):
        self.scout = scout
        self.queen = queen
        self.is_waypoint = is_poi
        self.is_current = is_current
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.time = time
        self.needs_transmit = needs_transmit

    def mongo_dict(self):
        return {
            'scout': self.scout,
            'queen': self.queen,
            'time': self.time,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'isCurrent': self.is_current,
            'isWaypoint': self.is_waypoint,
            'needsTransmit': self.needs_transmit,
            'description': self.description
        }

class Model(object):

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.database = self.client.beacon #rename this based on the database
        self.points = self.database.points

    def add_location_data_point(self,scout,queen,slat,slon,time):
        data = DataPoint(scout, queen, False, True, slat,slon,None,time,True)
        self.points.update_many(
            {'scout': data.scout, 'queen': data.queen, 'isCurrent':True },
            {'$set': {'isCurrent': False}}
        )
        self.points.insert_one(data.mongo_dict())

    def add_poi_data_point(self,scout,queen,plat,plon,time,description):
        data = DataPoint(scout, queen, True, None, plat, plon, description, time, True)
        self.points.insert_one(data.mongo_dict())

    def add_hive_data_point(self, scout, queen, is_poi, is_current, latitude, longitude, description, time):
        data = DataPoint(scout, queen, is_poi, is_current, latitude, longitude, description, time, None)
        self.points.insert_one(data.mongo_dict())

    def location_data_to_send(self):
        data = []
        ids = []
        for point in self.points.find({'isWaypoint': False, 'needsTransmit': True}).limit(5):
            data.append(point)
            ids.append(point['_id'])
        self.points.update_many({'_id':{'$in': ids}}, {'$set':{'needsTransmit': False}})
        return data

    def poi_data_to_send(self):
        data = self.points.find_one({'isWaypoint': True,'needsTransmit': True})
        if data is None:
            return None
        self.points.update_one({'_id': data['_id']},{'$set':{'needsTransmit': False}})
        return data
