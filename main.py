"""

PMEC final project
Team: Python Run
Team Members: Jade Sauvé
              Joshua Sacks
              Maria Kuruvilla
              Irita Aylward

Main body of the project


TO DO

add the module that will create a folder for the data/figures  x
add some input from user
make all paths relative
add the folder/station as an option in the function
prep the data for the first year for comparison with chosen year
get one year of data, dateitme object

"""

# Modules
import ftplib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

import os
import sys
pht = os.path.abspath('.')
if pht not in sys.path:
    sys.path.append(pht)
from modules import *


######################## Parameters ########################

#year = range(2005,2013)
extension = ['.A1','.B1','.C1','.D1','.E1','.F1','.G1','.H1'] # 2005-2012
#day_of_year = range(365)
year = [2009]
day_of_year = [202]
# one or many ?????

# Saving the plots
#save = True  # True or False, to save
#directory_out = ''
#file_out = ''
#directory to save the data files
#out_dir = ''
##############################################################

# User input
print('Please select a year between 2005 and 2012')
year = input("Year: ")
while year not in range(2005,2013):
    print('WARNING Your selection is not aaceptable!')
    print('Please select a year between 2005 and 2012')
    year = input("Year: ")

print('Please select a day between 1 and 365')
day_of_year = input("Day of the year: ")
while day_of_year not in range(1,366):
    print('WARNING Your selection is not aaceptable!')
    print('Please select a day between 1 and 365')
    day_of_year = input("Day of the year: ")


## make sure the output directory exists
this_dir = os.path.abspath('.').split('/')[-1]
this_parent = os.path.abspath('.').split('/')[-2]
out_dir = this_parent + '_output/'
print('Creating ' + out_dir + ', if needed')
make_dir(out_dir)

print(out_dir)

#This section of code uses the 'retrieve_data' function to interact with the website
#and put the files into the output directory
#clutch is a list of the filenames created to then read those ASCII files back in for further analysis
clutch = []
for i in year:
    for j in day_of_year:
        for k in extension:
            filename = retrieve_data(str(i), '{0:03}'.format(j), k, out_dir)
            clutch.append(filename)
            print(filename)


#This sections of code uses the 'pyrun_parse' function to convert the ASCII files
#the code is run in a loop to process all of the ASCII files for the given day
#run is the final DataFrame created, duplicates observations are removed.
df=pd.DataFrame(columns = {"date", "time", "ID"})
for c in clutch:
    fish = pd.DataFrame(pyrun_parse(out_dir+c))
    df = pd.merge(df, fish, how='outer')
df = df.drop_duplicates()
# add pd.reset_index to resetn the index or make the date a datetime object and then the axis -  more funcionality then
#print(df)


df = df.drop_duplicates(subset=['ID']) # keep only the fist instance of a Tag ID
df['datetime'] = pd.to_datetime(df['date']+df['time'], format='%m/%d/%y%H:%M:%S') # create a datetime object
df = df.set_index('datetime').drop(['time', 'date'], axis=1) # make the new datetime object an index and drop the old 'date' and 'time' columns
print(df)
