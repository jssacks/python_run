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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import datetime

import os
import sys
pht = os.path.abspath('/../python_run')
if pht not in sys.path:
    sys.path.append(pht)
from modules import *


######################## Parameters ########################

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
#directory_in = ''  


#save = True  # True or False, to save
#directory_out = ''
#file_out = ''  
#directory to save the data files
#out_dir = ''
##############################################################


############################################################## RETRIEVING DATA ###############################################

"""
ftp://ftp.ptagis.org/RawDataFiles/Interrogation/Loaded/158/2011/

"""

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

year = range(2005,2013)
extension = ['.A1','.B1','.C1','.D1','.E1','.F1','.G1','.H1']
day_of_year = range(365)
year = [2010]
day_of_year = [201]
for i in year:
	for j in day_of_year:
		for k in extension:
			filename = retrieve_data(str(i), '{0:03}'.format(j), k)
			print(filename)
			#it seems like BO1 does not have the data that we want, but you can just change 'folder' depending on what station we choose 

			#df = pd.read_csv(out_dir+filename,delim_whitespace=True, skiprows=4, skipfooter = 3, engine = 'python')#last argument might not be required
clutch = []
    for i in year:
        for j in day_of_year:
            for k in extension:
                filename = retrieve_data(str(i), '{0:03}'.format(j), k)
                clutch.append(filename)





