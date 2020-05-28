"""

PMEC final project
Team: Python Run
Team Members: Jade Sauvé
              Joshua Sacks
              Maria Kuruvilla
              Irita Aylward

Contains the modules used in main_body.py

"""

# Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import shutil
import ftplib
#import datetime

#Curtesy of Parker, to create a new directory
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


def retrieve_data(year, day_of_year, extension, out_dir):
    """
    downloads the ASCII files from the website for a specific year and day
    """
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

    # this is bad form, specify an error type
    except:
        print(' -- Failed to retrieve' + filename)
        #pass


def pyrun_parse(filename):
    """
    extracts the date, time, and ID for the observations from the ASCII files
    and outputs this information into a pandas DataFrame  
    """
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
        return None
