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

directory_in = ''  
file_geo = '/Users/jadesauve/Desktop/PTAGIS_GIS_Data.gdb'

save = True  # True or False, to save
directory_out = ''
file_out = ''  

##############################################################

# # read in geodatabase
# import fiona
# import geopandas as gpd

# fiona.listlayers(file_geo)

# # Download from https://data.cityofnewyork.us/City-Government/Projected-Sea-Level-Rise/6an6-9htp directly...
# data = gpd.read_file(file_geo, driver='FileGDB', layer=1)



"""
Notes:

https://api.ptagis.org/Swagger/ui/index#/

an xml file...
ftp://ftp.ptagis.org/RawDataFiles/Interrogation/Loaded/ACM/2020/ACM-2020-002-P-001.xml
"""





