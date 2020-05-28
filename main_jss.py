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
pht = os.path.abspath('/../python_run')
if pht not in sys.path:
    sys.path.append(pht)


#Function stolen from Parker to create a new directory
def make_dir(dirname, clean=False):
    """
    Make a directory if it does not exist.
    Use clean=True to clobber the existing directory.
    """
    if clean == True:
        shutil.rmtree(dirname, ignore_errors=True)
        os.mkdir(dirname)
    else:
        try:
            os.mkdir(dirname)
        except OSError:
            pass # assume OSError was raised because directory already exists

## make sure the output directory exists
this_dir = os.path.abspath('.').split('/')[-1]
this_parent = os.path.abspath('.').split('/')[-1]
out_dir = this_parent + '_output/'
print('Creating ' + out_dir + ', if needed')
make_dir(out_dir)

print(out_dir)

"""
This is the functions section of the code (which we will likely want to turn into a module)
the two functions currently are 
1. 'retrieve_data' which downloads the ASCII files from the website for a specific year and day
2. 'pyrun_parse' which extracts the date, time, and ID for the observations from the ASCII files
and outputs this information into a pandas DataFrame  
"""
#functions: 
    #retrieve_data
def retrieve_data(year = '2005', day_of_year = '101', extension = '.A1'):
    try:
        folder = 'BO1/' # name of the folder in which contains the file you want (also the name of the damn)
        year = year + '/' 
        path = 'RawDataFiles/Interrogation/Loaded/' + folder + year #latter part of the url (path to file in the website)
        filename = folder[0:-1] + year[2:-1] + day_of_year + extension #'15811333.INT' #name of the file we want to download
        # first three digits are name of the folder, next 2 indicated the year
        #and the last three indicate day of year. This can be put in a loop.
        ftp = ftplib.FTP("ftp.ptagis.org") #server IP of the website we want to download from
        ftp.login() #we do not need username and password for this data
        ftp.cwd(path) #change currect working path on the website to the location where the file is
        ftp.retrbinary("RETR " + filename ,open(out_dir+filename, 'wb').write) 
        ftp.quit()
        return(filename)

        print(' Retrieved ' + filename)   
        
    except:
        print(' -- Failed to retrieve' + filename)
        pass

#pyrun_parse
def pyrun_parse(filename): #function to read the individual ASCII files and turn them into a Pandas DataFrame
    try:
        z = [] #list to read dictionaries created from each line of the file into 
        f = open(filename, 'r')
        for line in f:
            line = line.strip() #removes hidden characters
            columns = line.split(" ") #splits lines into columns based on whitespace 
            source = {} #a dictionary to put the 2 columns created from each line into
            source['x'] = columns[0] #the first column for each line is given the key "x"
            source['a'] = columns[1:8] #the remaining columns are a list corresponding to key "a"
            z.append(source) #the dictionary of "x:__; a:_________" for each line is added to list z creating a list of dictionaries

        z2 = pd.DataFrame(z) #convert list of dicts z to a pandas DataFrame
        
        z3 = z2[z2.x == '|'] #only keep lines containing observations (marked with a '|' in column "x")
    
        dat = z3['a'].apply(pd.Series) #create a new DataFrame only containing the actual observation info
        dat = dat.rename(columns = lambda x : 'dat_' + str(x)) #rename the columns
        zat = dat[['dat_1', 'dat_2', 'dat_3']] #only keep the columns corresponding to date, time, and ID
        zat = zat.rename(columns = {'dat_1': "date", 'dat_2': "time", 'dat_3': "ID"}) #rename these columns
        zat2 = zat[~zat['ID'].str.contains("0000")] #remove test tag observations
          
        print("\nThe salmon evaded all of the grizzles and ran all the way up the stream") #it worked
        return zat2

    
    except:
        print("The salmon got eaten by a hungry grizzly bear") #it did not work


#End of functions 
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
print(run)