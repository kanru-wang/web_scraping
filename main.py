# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 20:41:17 2018

@author: Kevin
"""

import glob
import csv
import pandas as pd
import web_scraping_red_wine as red_wine

#for e in ['red_wine','white_wine','sparkling','spirit',
#          'pre-mixed','beer_and_cider']:    
old_csv = glob.glob('*red_wine.csv')[0]
print(old_csv)

df = pd.read_csv(old_csv, index_col = 'product_name')

df_updated = pd.concat([df, red_wine.df_new], axis = 1)

#with open (old_csv, 'r') as csv_file:
#    csv_reader = csv.reader(csv_file)
#    for line in csv_reader:
#        print(line)

## "today" is the col name of the new col to be added to the existing df.
#now = datetime.datetime.now()
#today = str(now.strftime("%Y-%m-%d"))
#
#csv_file = open('{}.csv'.format(today), 'w', newline = '') 
#
#csv_writer = csv.writer(csv_file)
#csv_writer.writerow(['product_name', today])
#
#
#
#csv_file.close()