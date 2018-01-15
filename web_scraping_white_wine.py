# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 16:58:34 2018

@author: Kevin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

"""
White wine url: 
    Dan Murphy's (not Connections). 
    Price 5 - 30.
    Product 1 to 120. Then product 121 to 240.
"""

# "today" is the col name of the new col to be added to the existing df.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

df_new = pd.DataFrame(columns = [today])

source1 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '25918%7D%2F5.0%3Cprice%3C30.0%2Fweb_dsv_flag%3E%7Bdan'
                       '20murphy27s%7D%26fh_view_size%3D120%26fh_start_index%'
                       '3D0%26fh_sort%3D-sales_value_30_days%26fh_modificatio'
                       'n%3D%2528secondid%253C%257Bdm_b999999000632%257D%252C'
                       'blocked%2529%252C%2528secondid%253C%257Bdm_mystery57%'
                       '257D%252Cblocked%2529%252C%2528secondid%253C%257Bdm_m'
                       'ystery52%257D%252Cblocked%2529%252C%2528secondid%253C'
                       '%257Bdm_757646%257D%252Cblocked%2529%252C%2528secondi'
                       'd%253C%257Bdm_610528%257D%252Cblocked%2529%252C%2528s'
                       'econdid%253C%257Bdm_786481%257D%252Cblocked%2529%252C'
                       '%2528secondid%253C%257Bdm_616722%257D%252Cblocked%252'
                       '9%252C%2528instock%253D0%252Cbottom%2529%26fh_maxdisp'
                       'laynrvalues_categories%3D-1&resetnav=false&mfRefsh=fa'
                       'lse&storeExclusivePage=false').text

source2 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '25918%7D%2F5.0%3Cprice%3C30.0%2Fweb_dsv_flag%3E%7Bdan'
                       '20murphy27s%7D%26fh_view_size%3D120%26fh_start_index%'
                       '3D120%26fh_sort%3D-sales_value_30_days%26fh_modificat'
                       'ion%3D%2528secondid%253C%257Bdm_b999999000632%257D%25'
                       '2Cblocked%2529%252C%2528secondid%253C%257Bdm_mystery5'
                       '7%257D%252Cblocked%2529%252C%2528secondid%253C%257Bdm'
                       '_mystery52%257D%252Cblocked%2529%252C%2528secondid%25'
                       '3C%257Bdm_757646%257D%252Cblocked%2529%252C%2528secon'
                       'did%253C%257Bdm_610528%257D%252Cblocked%2529%252C%252'
                       '8secondid%253C%257Bdm_786481%257D%252Cblocked%2529%25'
                       '2C%2528secondid%253C%257Bdm_616722%257D%252Cblocked%2'
                       '529%252C%2528instock%253D0%252Cbottom%2529%26fh_maxdi'
                       'splaynrvalues_categories%3D-1&resetnav=false&mfRefsh='
                       'false&storeExclusivePage=false').text
                       
soup1 = BeautifulSoup(source1, 'lxml')
soup2 = BeautifulSoup(source2, 'lxml')

def extract(soup, df_new):
    for product in soup.find_all('div', 
                                 {'class':'independent-product-module'}):
        product_name = product.div.h2.a['title']
        # Replace Frech letters with English
        translationTable = str.maketrans("éëàèùâêîôóûç", "eeaeuaeioouc")
        product_name = product_name.translate(translationTable)
        try:
            price = product.find_all('li', {'class':'price-secondary'})[0]\
                    .p.span.text
        except IndexError:
            price = product.find_all('span',{'class':'price'})[0].text
        price = price.replace('$','')
        
        df_new.loc[product_name] = price
    
    return df_new 

df_new = extract(soup = soup1, df_new = df_new)
df_new = extract(soup = soup2, df_new = df_new)    
