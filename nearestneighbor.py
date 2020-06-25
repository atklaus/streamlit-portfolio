import pandas as pd
import numpy as np
import os
import savReaderWriter as spss_reader
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime
import itertools
import inspect
from enum import Enum
import pgeocode as geo
import unicodedata
import sys
reload(sys)  
sys.setdefaultencoding('Cp1252')
import time
import geopy
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import pyodbc

os.chdir('C:\\\\Users\\klausa\\Desktop\\Offline\\BetaScript Ideas')

db_list = list(pd.read_excel('C:\\\\Users\\klausa\\Desktop\\Offline\\BetaScript Ideas\\ipedsDB.xlsx')['Name'])


conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\\\Users\\klausa\\Desktop\\Offline\\BetaScript Ideas\\IPEDS201819.accdb;')
# cursor = conn.cursor()
# cursor.execute('select * from ADM2018')

master_df = pd.read_sql('select * from ADM2018', conn)
master_df = master_df[['UNITID']]


for table in db_list:
    df = pd.read_sql("""select * from """ + table + """  """, conn)

    try:
        if len(df) < 5000:
            master_df = pd.merge(master_df, df,  how='left', left_on=['UNITID'], right_on=['UNITID'])
    except:
        print('join failed')

name_df = pd.read_excel('UNITID Crosswalk.xlsx')

master_df = pd.merge(master_df, name_df,  how='left', left_on=['UNITID'], right_on=['UNITID'])

master_df.to_csv('ipeds_2018.csv', index = False)



from scipy.spatial import distance
a = (1, 2, 3)
b = (4, 5, 6)
dst = distance.euclidean(a, b)




