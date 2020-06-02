"""

PMEC final project
Team: Slamin' Salmons
Team Members: Jade Sauvé
              Joshua Sacks
              Maria Kuruvilla
              Irita Aylward

Contains the modules used in main.py

"""

# Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import shutil
import ftplib
import timeit
import signal


def warningfct():
    """
    this function prints some warnings
    """
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('WARNING Your selection is not valid!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print()


def user_input():
    """
    asks for year and day_of_year from the user
    """
    print()
    print('Please select a year between 2005 and 2012')
    print()
    year = input("    Year: ")
    # makes sure the year is as expected
    while int(year) not in range(2005,2013):
        warningfct()
        print('Please select a year between 2005 and 2012')
        print('Note that 2009 is a good year.')
        print()
        year = input("  Year: ")
        print()
    year = [int(year)]
    print()
    print('1. Plot one year of data - this will be significantly longer')
    print('2. Plot one day of data')
    print()
    range_choice = input('  Please enter 1 or 2: ')
    print()

    while range_choice not in ['1','1.','2','2.']:
        warningfct()
        print('1. Plot one year of data')
        print('2. Plot one day of data')
        print()
        range_choice = input('  Please enter 1 or 2: ')

    if range_choice in ['1','1.']:
        # from 1 to 365 included
        day_of_year = range(1,366)
    elif range_choice in ['2','2.']:
        print('Please select a day between 1 and 365')
        print('Note that for 2009, day 202 is a good choice.')
        print()
        day_of_year = input("    Day of the year: ")
        print()
        while int(day_of_year) not in range(1,366):
            warningfct()
            print('Please select a day between 1 and 365')
            print()
            day_of_year = input("   Day of the year: ")
        day_of_year = [int(day_of_year)]

    return year, day_of_year, range_choice


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


def retrieve_data(year, day_of_year, extension, out_dir, station='BO1'):
    """
    downloads the ASCII files from the website for a specific year and day
    """
    # Set it up so if it takes too long, it will exit by itself
    # Register an handler for the timeout
    def handler(signum, frame):
        #print("Forever is over!")
        raise Exception("Taking too long...")
    # Register the signal function handler
    signal.signal(signal.SIGALRM, handler)
    # Define a timeout for your function in seconds
    signal.alarm(10)

    folder = station + '/' # name of the folder in which contains the file you want (also the name of the damn)
    year = year + '/'
    path = 'RawDataFiles/Interrogation/Loaded/' + folder + year #latter part of the url (path to file in the website)
    filename = folder[0:-1] + year[2:-1] + day_of_year + extension #'15811333.INT' #name of the file we want to download
    # first three digits are name of the folder, next 2 indicated the year
    #and the last three indicate day of year. This can be put in a loop.
    try:
        ftp = ftplib.FTP("ftp.ptagis.org") #server IP of the website we want to download from
        ftp.login() #we do not need username and password for this data
        ftp.cwd(path) #change current working path on the website to the location where the file is
        ftp.retrbinary("RETR " + filename ,open(out_dir+filename, 'wb').write)
        ftp.quit()
        print(' Retrieved ' + filename)
        # cancel the timer
        signal.alarm(0)
        return filename

    except Exception: #, exc
        print('Taking too long...')
        print(' -- Failed to retrieve ' + filename)
        return None
    # this is bad form, specify an error type
    except:
        print(' -- Failed to retrieve ' + filename)
        # cancel the timer
        signal.alarm(0)
        return None



def pyrun_parse(filename):
    """
    extracts the date, time, and ID for the observations from the ASCII files
    and outputs this information into a pandas DataFrame
    """
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
    return zat2


def specify_plot_range(range_choice, df, date, out_path):
    '''
    Function that asks the user how they'd like to plot the data,
    then calls on other functions to make a binned dataframe and plot the data
    '''
    print(f"\nNow we'll plot the data that we just retrieved.\n")

    if range_choice in ['1','1.']: # if user retrieved 1 YEAR of data
        print('Would you like to plot the data by:\n\t1. Hour\n\t2. Day\n\t3. Month')
        print('(please enter 1, 2, or 3)') # user selects plotting by Hour, Day, or Month
        plot_range_input = input('  > ')
        while plot_range_input not in ['1','1.','2','2.','3','3.']:
            print("Your input is invalid.\nPlease enter 1, 2, or 3)")
            plot_range_input = input('  > ')

        # assign variables depending on the user-selected plotting method
        if plot_range_input in ['1','1.']:
            increment_max, increment_label, time_index = 25, 'hour', df.index.hour
        elif plot_range_input in ['2','2.']:
            increment_max, increment_label, time_index = 32, 'day', df.index.day
        elif plot_range_input in ['3','3.']:
            increment_max, increment_label, time_index = 13, 'month', df.index.month

    elif range_choice in ['2','2.']: # if user retrieved 1 DAY of data, plot by the hour
        increment_max, increment_label, time_index = 25, 'hour', df.index.hour

    # get user input for size of time bins
    bin_input = get_bin_input(0, increment_max, increment_label)
    # make a binned dataframe based on selected bin size
    new_df = make_binned_df(time_index, 0, increment_max, bin_input, df)
    # print max and min
    print(f'The max number of fish recorded in a given interval was: {new_df.max()[0]}\nThe minimum was: {new_df.min()[0]}')
    # plot the data
    plot_data(new_df, increment_label, date, bin_input, out_path)

    return new_df



def make_binned_df(time_index, range_start, range_end, bin_size, df):
    '''
    Makes a new dataframe with grouped time intervales as indices,
    and number of fish occurences within an interval as the values
    '''
    # makes an array based on range start and stop, with bin_size as the step-size
    range_arr = np.arange(range_start, range_end, bin_size)

    # if the last element in the range array falls short of what the end should be (range_end),
    # then add an end value to the array. Without this, it cuts off the last days/hours of data
    # if the user selects a bin_size that is not a factor of the range_end-1.
    # But this can also makes the last bin a different size than the others.
    if range_arr[-1] != range_end - 1:
        range_arr = np.append(range_arr, [range_end - 1])
    # creation of new 'binned' dataframe
    df_bins = df.groupby(pd.cut(time_index, range_arr)).count()

    return df_bins # this is the dataframe that gets plotted.


def get_bin_input(range_start, range_end, unit):
    '''
    Gets user input for the size bin they want to use.
    '''
    print(f"Enter the size of the time intervals you'd like to use for plotting (enter an integer number of {unit+'s'} between {range_start+1} and {range_end-1})")
    bin_input = int(input(' > '))
    while bin_input not in range(range_start, range_end):
        print(f"Your input is invalid.\nPlease enter a valid interval size (enter an integer between {range_start+1} and {range_end-1})")
        bin_input = int(input(' > '))
    return bin_input


def plot_data(df, unit, date, bin_input, out_path):
    '''
    Function for plotting the data. Produces a bar graph of fish interrogation vs time.
    '''
    fs = 14 # font size
    plt.close('all')
    fig, ax = plt.subplots(figsize = (8,8))
    df.plot(kind="bar", fc = 'salmon', ec = 'k', fontsize = .9*fs, legend =False, ax = ax)
    ax.set_title(f'Fish Interrogation', size= 1.5*fs)
    ax.set_xlabel(f'Time Interval ({unit})', size = 1.2*fs)
    ax.set_ylabel('Number of Fish', size = 1.2*fs)
    ax.set_yticks([]) # get rid of ticks/labels on y axis
    # make a text box that shows the year, interval length in the top-right corner
    ax.text(.95, .88, f'Year: {date[0]}' + ('' if np.isnan(date[1]) else '\nDay: ' + str(date[1])) + f'\nInterval: {bin_input} {unit}(s)',
        fontsize=fs, transform = ax.transAxes,ha='right', bbox=dict(facecolor='lightsalmon', edgecolor='None', alpha=0.5))
    # show the frequency on top of each bar
    for index, value in enumerate(df['ID']):
        plt.text(index-.13, value+0.04, value, fontsize = .8*fs)
    ax.set_ylim([0,df.max()[0]*1.2])
    plt.tight_layout()
    # filename for the saved plot
    file_out='bargraph_+'+str(date[0])+'_'+unit+'_'+str(bin_input)+'.eps'
    plt.savefig(out_path+file_out,format='eps',dpi=200)
    plt.show()
