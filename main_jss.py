# -*- coding: utf-8 -*-
"""
PMEC final project
Team: Python Run
Team Members: Jade Sauvé
			  Joshua Sacks
			  Maria Kuruvilla
			  Irita Aylward

Main body of the project

"""


# Modules
import ftplib
import pandas as pd
import matplotlib.pyplot as plt
#import datetime

import os
import sys
import shutil
pht = os.path.abspath('.')
if pht not in sys.path:
    sys.path.append(pht)
from modules import *


## make sure the output directory exists
this_dir = os.path.abspath('.').split('/')[-1]
this_parent = os.path.abspath('.').split('/')[-2]
out_dir = this_parent + '_output/'
print('Creating ' + out_dir + ', if needed')
make_dir(out_dir)

print(out_dir)


"""
This following section of code features our input values and the actual use of the functions

Currently, the output data structure is called "run" and it is a merged DataFrame of 
all unique observations of time and fish (ID) for a given day.

"""
##input values
year = range(2005,2013)
extension = ['.A1','.B1','.C1','.D1','.E1','.F1','.G1','.H1']
day_of_year = range(365)
year = [2009]
day_of_year = [202]


#This section of code uses the 'retrieve_data' function to interact with the website 
#and put the files into the output directory
#clutch is a list of the filenames created to then read those ASCII files back in for further analysis 
clutch = []
for i in year:
    for j in day_of_year:
        for k in extension:
            filename = retrieve_data(str(i), '{0:03}'.format(j), k)
            clutch.append(filename)
            print(filename)

#This sections of code uses the 'pyrun_parse' function to convert the ASCII files
#the code is run in a loop to process all of the ASCII files for the given day
#run is the final DataFrame created, duplicates observations are removed. 
run=pd.DataFrame(columns = {"date", "time", "ID"})
for c in clutch:
    fish = pd.DataFrame(pyrun_parse(out_dir+c))
    run = pd.merge(run, fish, how='outer')
run = run.drop_duplicates()
# add pd.reset_index to resetn the index or make the date a datetime object and then the axis -  more funcionality then 
print(run)