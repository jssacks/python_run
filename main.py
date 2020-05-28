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
#import datetime

import os
import sys
pht = os.path.abspath('.')
if pht not in sys.path:
    sys.path.append(pht)
from modules import *


######################## Parameters ########################

#year = range(2005,2013)
# File extensions for the years 2005 to 2012
extension = ['.A1','.B1','.C1','.D1','.E1','.F1','.G1','.H1'] 
#day_of_year = range(365)
#year = [2009]
#day_of_year = [202]
# one or many ?????

# Saving the plots
#save = True  # True or False, to save
#directory_out = ''
#file_out = ''
#directory to save the data files
#out_dir = ''
##############################################################

# User input 
print()
print('Please select a year between 2005 and 2012')
print()
year = input("    Year: ")
while int(year) not in range(2005,2013):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('WARNING Your selection is not acceptable!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print()
    print('Please select a year between 2005 and 2012')
    print()
    year = input("Year: ")
    print()
year = [int(year)]

print()
print('Please select a day between 1 and 365')
print()
day_of_year = input("    Day of the year: ")
print()
while int(day_of_year) not in range(1,366):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('WARNING Your selection is not acceptable!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print()
    print('Please select a day between 1 and 365')
    print()
    day_of_year = input("Day of the year: ")
day_of_year = [int(day_of_year)]


## make sure the output directory exists
this_path = os.path.abspath('.')
this_dir = this_path.split('/')[-1]
this_parent = this_path.split('/')[-2]
out_dir = this_parent + '_output/'
print('Creating ' + out_dir + ', if needed')
make_dir(out_dir)

#print(out_dir)

# This section of code uses the 'retrieve_data' function to interact with the website 
# and put the files into the output directory
# clutch is a list of the filenames created to then read those ASCII files back in for further analysis 
clutch = []
for i in year:
    for j in day_of_year:
        for k in extension:
            filename = retrieve_data(str(i), '{0:03}'.format(j), k, out_dir)
            clutch.append(filename)
            print(filename)


# This sections of code uses the 'pyrun_parse' function to convert the ASCII files
# the code is run in a loop to process all of the ASCII files for the given day
# df is the final DataFrame created, duplicates observations are removed. 
df=pd.DataFrame(columns = {"date", "time", "ID"})
for c in clutch:
    fish = pyrun_parse(out_dir+c)
    # only merge is there is data to merge
    if fish is not None:
        df = pd.merge(df, fish, how='outer')
# check if the df is empty / no data on this date
if df.empty:
    print()
    print('There is no data for this date.')
    print()
    print('Would you like to choose another date?')
    print()
    decision = input('Y or N:  ')
    if decision is 'Y':
        # rerun this script from the beginning
        os.execv('./main.py', sys.argv)

# if the df is not empty, move on
else:
    # remove duplicate entries
    df = df.drop_duplicates()

    # make a column of date time objects
    date_col = pd.to_datetime(df['date']+'/'+df['time'], format='%m/%d/%y/%H:%M:%S')
    date_col = date_col.rename('datetime_obj')

    # add this column to the df
    df = pd.concat([df, date_col],axis=1)
    # set this column as the index
    df = df.set_index('datetime_obj')
    
    # removes the date and time columns
    df.drop(['date','time'],axis=1,inplace=True)

    """
    to obtain the year of a datetime_obj do .what_you_want (.year, .day)
    as an example:
        df.index[0].day 

    for binning consider pd.cut() used with grouby()

    https://stackoverflow.com/questions/51250554/pandas-bin-and-sum
    """


















