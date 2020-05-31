"""

PMEC final project
Team: Slamin' Salmons
Team Members: Jade Sauvé
              Joshua Sacks
              Maria Kuruvilla
              Irita Aylward

Main body of the project


"""

# Modules
#import ftplib
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
year, day_of_year, range_choice = user_input()

## make sure the output directory exists
this_path = os.path.abspath('.')
this_dir = this_path.split('/')[-1]
this_parent = os.path.abspath('../.')
# directory name
out_dir = this_dir + '_output/'
# directory name
out_path = os.path.join(this_parent,out_dir)
print('Creating ' + out_dir +' and deleting the old one')
print()
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
    #print(c)
    fish = pyrun_parse(out_path+c)
    # only merge if there is data to merge
    if fish is not None:
        df = pd.merge(df, fish, how='outer')
        a=a+1
    else:
        b=b+1
#Print how many files had data or not
print()
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
    df = df.drop_duplicates(subset=['ID'])

    # make a column of date time objects
    date_col = pd.to_datetime(df['date']+'/'+df['time'], format='%m/%d/%y/%H:%M:%S')
    date_col = date_col.rename('datetime_obj')

    # add this column to the df
    df = pd.concat([df, date_col],axis=1)
    # set this column as the index
    df = df.set_index('datetime_obj')

    # removes the date and time columns
    df.drop(['date','time'],axis=1,inplace=True)

    # print the number of unique entries in the df
    print(f'\n{len(df)} unique fish entries were recorded during your selected time frame. Cool!')

    # Plot
    date = [year[0], np.nan if len(day_of_year)>1 else day_of_year[0]] 
    specify_plot_range(range_choice, df, date)

    # we need to save the figure



