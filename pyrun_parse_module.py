# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:33:20 2020

@author: joshu
"""


import pandas as pd

filename1 = r"C:\Users\joshu\Documents\GitHub\python_run_output\BO110201.D1"

def pyrun_parse(filename):
    try:
        z = []
        f = open(filename, 'r')
        for line in f:
            line = line.strip()
            columns = line.split(" ")
            source = {}
            source['x'] = columns[0]
            source['a'] = columns[1:8]
            z.append(source)

        z2 = pd.DataFrame(z)


        z3 = z2[z2.x == '|']
    
        dat = z3['a'].apply(pd.Series)
        dat = dat.rename(columns = lambda x : 'dat_' + str(x))
        zat = dat[['dat_1', 'dat_2', 'dat_3']]
        zat = zat.rename(columns = {'dat_1': "date", 'dat_2': "time", 'dat_3': "ID"})


        zat2 = zat[~zat['ID'].str.contains("0000")]
  
        print("\nThe salmon evaded all of the grizzles and ran all the way up the stream")
        return zat2

    
    except:
        print("The salmon got eaten by a hungry grizzly bear")
        
fly = pyrun_parse(filename1)
#print(fly)