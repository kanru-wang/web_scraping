# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 20:41:17 2018

@author: Kevin
"""

import glob
import pandas as pd
import datetime
import web_scraping_red_wine as red_wine
import web_scraping_white_wine as white_wine
import web_scraping_sparkling_wine as sparkling
import web_scraping_spirit as spirit
import web_scraping_premixed as premixed
import web_scraping_beer_and_cider as beer_and_cider

# "today" is a part of the csv file name.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

product_dict =  {'red_wine': red_wine.df_new,
                 'white_wine': white_wine.df_new,
                 'sparkling': sparkling.df_new,
                 'spirit': spirit.df_new,
                 'premixed': premixed.df_new,
                 'beer_and_cider': beer_and_cider.df_new
                 }

#df_lowest_price = pd.DataFrame()

def checkIfLowest(row):
    # If this week's price is lower than the previous, say, 12 week's prices,
    # return the whole row.
    # When summing, TRUE becomes 1, FALSE becomes 0.
    
    # Need to deal with Null values in row in the future. The more NaN,
    # the fewer Trues inside sum( ).
    
    # Shouldn't be (row[-1] <= row[-13:-1]), since many products never change.
    
    if sum(row[-1] < row[-13:-1]) > 5: #Should be > 12
        #return row
        print(row)
    
for e in ['red_wine','white_wine','sparkling','spirit',
          'premixed','beer_and_cider']:    
    old_csv = glob.glob('*{}.csv'.format(e))[0]
    print("Doing " + old_csv)
    df = pd.read_csv(old_csv, index_col = 0)
    df_updated = pd.concat([df, product_dict[e]], axis = 1)
    df_updated.to_csv('{}.csv'.format(today + '_' + e))

    df_lowest_price_this_type = df_updated.apply(checkIfLowest, axis = 1)#.dropna()
    #df_lowest_price = pd.concat([df_lowest_price, df_lowest_price_this_type], 
    #                            axis = 0)

#df_lowest_price.to_csv('{}.csv'.format(today + '_' + 'lowest_price'))
