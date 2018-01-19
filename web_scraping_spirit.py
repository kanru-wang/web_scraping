# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:49:31 2018

@author: Kevin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

"""
Whisky url (source1): 
    Category: Whiksy (to exclude premixed)
    Dan Murphy's (not Connections). 
    Price 1 - 100.
    Product 1 to 120.
    
Other Spirit url (source2):
    Category: Spirit (to exclude premixed)
    Dan Murphy's (not Connections). 
    Price 1 - 100.
    Product 1 to 120.
"""

# "today" is the col name of the new col to be added to the existing df.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

df_new = pd.DataFrame(columns = [today])

source1 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '84767%7D%2F1.0%3Cprice%3C100.0%2Fwebmaincategory%3E%7'
                       'Bwhisky%7D%2Fweb_dsv_flag%3E%7Bdan20murphy27s%7D%26fh'
                       '_view_size%3D120%26fh_sort%3D-sales_value_30_days%26f'
                       'h_modification%3D%2528secondid%253C%257Bdm_b999999000'
                       '632%257D%252Cblocked%2529%252C%2528secondid%253C%257B'
                       'dm_mystery57%257D%252Cblocked%2529%252C%2528secondid%'
                       '253C%257Bdm_mystery52%257D%252Cblocked%2529%252C%2528'
                       'secondid%253C%257Bdm_757646%257D%252Cblocked%2529%252'
                       'C%2528secondid%253C%257Bdm_610528%257D%252Cblocked%25'
                       '29%252C%2528secondid%253C%257Bdm_786481%257D%252Cbloc'
                       'ked%2529%252C%2528secondid%253C%257Bdm_616722%257D%25'
                       '2Cblocked%2529%252C%2528instock%253D0%252Cbottom%2529'
                       '%26fh_maxdisplaynrvalues_categories%3D-1&resetnav=fal'
                       'se&storeExclusivePage=false').text

source2 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '85866%7D%2Fwebmaincategory%3E%7Bspirits%7D%2Fweb_dsv_'
                       'flag%3E%7Bdan20murphy27s%7D%2F1.0%3Cprice%3C100.0%26f'
                       'h_view_size%3D120%26fh_start_index%3D0%26fh_sort%3D-s'
                       'ales_value_30_days%26fh_modification%3D%2528secondid%'
                       '253C%257Bdm_b999999000632%257D%252Cblocked%2529%252C%'
                       '2528secondid%253C%257Bdm_mystery57%257D%252Cblocked%2'
                       '529%252C%2528secondid%253C%257Bdm_mystery52%257D%252C'
                       'blocked%2529%252C%2528secondid%253C%257Bdm_757646%257'
                       'D%252Cblocked%2529%252C%2528secondid%253C%257Bdm_6105'
                       '28%257D%252Cblocked%2529%252C%2528secondid%253C%257Bd'
                       'm_786481%257D%252Cblocked%2529%252C%2528secondid%253C'
                       '%257Bdm_616722%257D%252Cblocked%2529%252C%2528instock'
                       '%253D0%252Cbottom%2529%26fh_maxdisplaynrvalues_catego'
                       'ries%3D-1&resetnav=false&mfRefsh=false&storeExclusive'
                       'Page=false').text
                       
soup1 = BeautifulSoup(source1, 'lxml')
soup2 = BeautifulSoup(source2, 'lxml')    

def extract(soup, df_new):
    for product in soup.find_all('div', 
                                 {'class':'independent-product-module'}):
        product_name = product.div.h2.a['title']
        # Replace Frech letters with English
        translationTable = str.maketrans("áàâäçéëèêÎîñöôóúûù",
                                         "aaaaceeeeiinooouuu")
        product_name = product_name.translate(translationTable)

        # Get a list of prices of different package sizes of this product.
        # Choose the lowest price.
        price_list = [x.text for x in 
                      product.find_all('span',{'class':'price'})]
        price_list_without_dollar = [x.replace('$','') for x in price_list]
        # To deal with some items that have no price displayed.
        try:
            min_price = min([float(x) for x in price_list_without_dollar])
        except ValueError:
            min_price = float('nan')
        
        df_new.loc[product_name] = min_price
    
    return df_new 

df_new = extract(soup = soup1, df_new = df_new)
df_new = extract(soup = soup2, df_new = df_new)
