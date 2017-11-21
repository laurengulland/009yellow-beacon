from tables import *

""" installed packages on linux:
$  sudo apt-get install libhdf5-serial-dev hdf5-tools h5utils
"""

# class Location_Point(scout_id,time,location_n,location_w):
#     hi = 0

class Location_Point():
    scout_id = Int64Col()
    time = Int64Col()
    location_n = Float64Col()
    location_w = Float64Col()

h5file = open_file("tutorial1.h5",mode='w',title="Test File")
root = h5file.root
group = h5file.create_group(root,'detector','Detector Information')
table = htfile.create_table(group,'readout',Location_Point,"Readout Example")




class Particle(IsDescription):
    identity = StringCol(itemsize=22, dflt=" ", pos=0)  # character String
    idnumber = Int16Col(dflt=1, pos = 1)  # short integer
    speed    = Float32Col(dflt=1, pos = 2)  # single-precision

#create the groups
group1 = fileh.create_group(root,'group1')
group2 = fileh.create_group(root,'group2')

#create an array in root group
# array1 = fileh.create_array(root, 'array1', ['string','array'], 'String array')

#create two new tables in group 1
table1 = fileh.create_table(group1,'table1',Particle)
table2 = fileh.create_table('/group2','table2',Particle)

# Create the last table in group2
array2 = fileh.create_array("/group1", "array2", [1,2,3,4])

# Now, fill the tables
for table in (table1, table2):
    # Get the record object associated with the table:
    row = table.row

    # Fill the table with 10 records
    for i in range(10):
        # First, assign the values to the Particle record
        row['identity']  = 'This is particle: %2d' % (i)
        row['idnumber'] = i
        row['speed']  = i * 2.

        # This injects the Record values
        row.append()

    # Flush the table buffers
    table.flush()

# Finally, close the file (this also will flush all the remaining buffers!)
fileh.close()
