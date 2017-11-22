# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 23:49:33 2017

@author: Joseph
"""

#test script for database

import sqlite3

## HEY MAKE SURE YOU CHANGE THIS
## THIS WILL CREATE THE DATABASE AT THE SPECIFIED FILEPATH
mydb = sqlite3.connect('C:/Users/Joseph/sqlite/beacon.db')
cursor = mydb.cursor()

# this creates the database schema
cursor.execute('''
CREATE TABLE QUEEN(
ID INT PRIMARY KEY NOT NULL
);
''')
mydb.commit()
cursor.execute('''
CREATE TABLE SCOUT(
ID INT NOT NULL,
QUEEN_ID INT NOT NULL,
PRIMARY KEY ( ID ),
FOREIGN KEY ( QUEEN_ID ) REFERENCES QUEEN( ID )
);
''')
mydb.commit()
cursor.execute('''
CREATE TABLE SCOUT_DATA_POINT(
SCOUT_ID INT NOT NULL,
LATITUDE REAL NOT NULL,
LONGITUDE REAL NOT NULL,
TIME INT NOT NULL,
NEEDS_TRANSMIT INT NOT NULL,
FOREIGN KEY ( SCOUT_ID ) REFERENCES SCOUT( ID )
);
''')
mydb.commit()
cursor.execute('''
CREATE TABLE POINT_OF_INTEREST(
SCOUT_ID INT NOT NULL,
LATITUDE REAL NOT NULL,
LONGITUDE REAL NOT NULL,
TIME INT NOT NULL,
NEEDS_TRANSMIT INT NOT NULL,
DESCRIPTION CHAR(60),
FOREIGN KEY ( SCOUT_ID ) REFERENCES SCOUT( ID )
);
''')
mydb.commit()
#this creates a queen
cursor.execute(
  'INSERT INTO QUEEN(ID) VALUES(:ID)',
  {'ID': 1}
)
#this creates scouts
cursor.execute(
  'INSERT INTO SCOUT(ID, QUEEN_ID) VALUES (:ID, :QUEEN_ID)',
  {'ID': 1, 'QUEEN_ID': 1}
)
mydb.commit()
cursor.execute(
  'INSERT INTO SCOUT(ID, QUEEN_ID) VALUES (:ID, :QUEEN_ID)',
  {'ID': 2, 'QUEEN_ID': 1}
)
mydb.commit()

#scout1 data
baselat = 42.358340
baselon = -71.094600
basetime = 1511327000
scout1lats = []
scout1lons = []
scout2lats = []
scout2lons = []
times = []
for i in range(0,10):
    scout1lats.append(baselat+0.00001*i)
    scout2lats.append(baselat-0.00001*i)
    scout1lons.append(baselon+0.00001*i)
    scout2lons.append(baselon-0.00001*i)
    times.append(basetime + 30*i)

# this creates visited scout locations
for i in range(0,10):
    cursor.execute(
      'INSERT INTO SCOUT_DATA_POINT(SCOUT_ID, LATITUDE, LONGITUDE, TIME, NEEDS_TRANSMIT) VALUES(?,?,?,?,?)',
      [1,scout1lats[i],scout1lons[i],times[i],1]
    )
    mydb.commit()
    cursor.execute(
      'INSERT INTO SCOUT_DATA_POINT(SCOUT_ID, LATITUDE, LONGITUDE, TIME, NEEDS_TRANSMIT) VALUES(?,?,?,?,?)',
      [2,scout2lats[i],scout2lons[i],times[i],1]
    )
    mydb.commit()

#this creates a couple POIs
cursor.execute(
  'INSERT INTO POINT_OF_INTEREST(SCOUT_ID,LATITUDE,LONGITUDE,TIME,NEEDS_TRANSMIT, DESCRIPTION) VALUES(?,?,?,?,?,?)',
  [1,scout1lats[2],scout1lons[2],times[2],1,'cape']
)
mydb.commit()
cursor.execute(
  'INSERT INTO POINT_OF_INTEREST(SCOUT_ID,LATITUDE,LONGITUDE,TIME,NEEDS_TRANSMIT, DESCRIPTION) VALUES(?,?,?,?,?,?)',
  [2,scout2lats[8],scout1lons[8],times[8],1,'mask']
)
mydb.commit()

cursor.execute('SELECT * FROM QUEEN')
print(cursor.fetchall())
cursor.execute('SELECT * FROM SCOUT')
print(cursor.fetchall())
cursor.execute('SELECT * FROM SCOUT_DATA_POINT')
print(cursor.fetchall())
cursor.execute('SELECT * FROM POINT_OF_INTEREST')
print(cursor.fetchall())
mydb.close()