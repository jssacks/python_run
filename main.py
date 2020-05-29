"""

PMEC final project
Team: Slamin' Salmons
Team Members: Jade Sauvé
              Joshua Sacks
              Maria Kuruvilla
              Irita Aylward

Main body of the project


TO DO

add the module that will create a folder for the data/figures  x
add some input from user  x
make all paths relative  x
add the folder/station as an option in the function  x
prep the data for the first year for comparison with chosen year
get one year of data  x
datetime object  x

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

# File extensions for the years 2005 to 2012
extension = ['.A1','.B1','.C1','.D1','.E1','.F1','.G1','.H1'] 


##############################################################

# User input 
year, day_of_year = user_input()

## make sure the output directory exists
this_path = os.path.abspath('.')
this_dir = this_path.split('/')[-1]
this_parent = os.path.abspath('../.')  
# directory name
out_dir = this_dir + '_output/'
# directory name
out_path = os.path.join(this_parent,out_dir)
print('Creating ' + out_dir +' and deleting the old one')
# make the dir, remove the old one
make_dir(out_path, clean=True)


# This section of code uses the 'retrieve_data' function to interact with the website 
# and put the files into the output directory
# clutch is a list of the filenames from the downloaded files
clutch = []
for i in year:
    for j in day_of_year:
        for k in extension:
            filename = retrieve_data(str(i), '{0:03}'.format(j), k, out_path)
            if filename is not None:
                clutch.append(filename)
                


# This sections of code uses the 'pyrun_parse' function to convert the ASCII files to a df
# the code is run in a loop to process all of the ASCII files for the given date
# initialize the df
df=pd.DataFrame(columns = {"date", "time", "ID"})
# initialize counters
a = b = 0
# for all files downloaded
for c in clutch:
    print(c)
    fish = pyrun_parse(out_path+c)
    # only merge if there is data to merge
    if fish is not None:
        df = pd.merge(df, fish, how='outer')
        a=a+1
    else:
        b=b+1
#Print how many files had data or not
print(str(a) +" salmon evaded all of the grizzlys and ran all the way up the stream")
print(str(b) +" salmon got eaten by a hungry grizzly bear")

# check if the df is empty, i.e. no data on this date/year
if df.empty:
    print()
    print('There is no data for this date range.')
    print()
    print('Would you like to choose another date?')
    print()
    decision = input('Y or N:  ')
    if decision is 'Y':
        # rerun this script from the beginning - doesnt always work sadly
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

















