# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:20:55 2018

@author: Kevin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

"""
Beer and cider url:
    Product 1 to 120. Then 121 to 240.
"""

# "today" is the col name of the new col to be added to the existing df.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

df_new = pd.DataFrame(columns = [today])

source1 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '25910%7D%26fh_view_size%3D120%26fh_start_index%3D0%26'
                       'fh_sort%3D-sales_value_30_days%26fh_modification%3D%2'
                       '528secondid%253C%257Bdm_b999999000632%257D%252Cblocke'
                       'd%2529%252C%2528secondid%253C%257Bdm_mystery57%257D%2'
                       '52Cblocked%2529%252C%2528secondid%253C%257Bdm_mystery'
                       '52%257D%252Cblocked%2529%252C%2528secondid%253C%257Bd'
                       'm_757646%257D%252Cblocked%2529%252C%2528secondid%253C'
                       '%257Bdm_610528%257D%252Cblocked%2529%252C%2528secondi'
                       'd%253C%257Bdm_786481%257D%252Cblocked%2529%252C%2528s'
                       'econdid%253C%257Bdm_616722%257D%252Cblocked%2529%252C'
                       '%2528instock%253D0%252Cbottom%2529%26fh_maxdisplaynrv'
                       'alues_categories%3D-1&resetnav=false&mfRefsh=false&st'
                       'oreExclusivePage=false').text

source2 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '25910%7D%26fh_view_size%3D120%26fh_start_index%3D120%'
                       '26fh_sort%3D-sales_value_30_days%26fh_modification%3D'
                       '%2528secondid%253C%257Bdm_b999999000632%257D%252Cbloc'
                       'ked%2529%252C%2528secondid%253C%257Bdm_mystery57%257D'
                       '%252Cblocked%2529%252C%2528secondid%253C%257Bdm_myste'
                       'ry52%257D%252Cblocked%2529%252C%2528secondid%253C%257'
                       'Bdm_757646%257D%252Cblocked%2529%252C%2528secondid%25'
                       '3C%257Bdm_610528%257D%252Cblocked%2529%252C%2528secon'
                       'did%253C%257Bdm_786481%257D%252Cblocked%2529%252C%252'
                       '8secondid%253C%257Bdm_616722%257D%252Cblocked%2529%25'
                       '2C%2528instock%253D0%252Cbottom%2529%26fh_maxdisplayn'
                       'rvalues_categories%3D-1&resetnav=false&mfRefsh=false&'
                       'storeExclusivePage=false'
                       ).text
                       
soup1 = BeautifulSoup(source1, 'lxml')
soup2 = BeautifulSoup(source2, 'lxml')    

def extract(soup, df_new):
    for product in soup.find_all('div', 
                                 {'class':'independent-product-module'}):
        product_name = product.div.h2.a['title']
        # Replace Frech letters with English
        translationTable = str.maketrans("áàâäçéëèêÎîñöôóúûùü",
                                         "aaaaceeeeiinooouuuu")
        product_name = product_name.translate(translationTable)
        
        # Get a list of prices of different package sizes of this product.
        # Choose the largest price.
        price_list = [x.text for x in 
                      product.find_all('span',{'class':'price'})]
        price_list_without_dollar = [x.replace('$','') for x in price_list]
        # To deal with some items that have no price displayed.
        try:
            max_price = max([float(x) for x in price_list_without_dollar])
        except ValueError:
            max_price = float('nan')
            
        df_new.loc[product_name] = max_price
    
    return df_new 

df_new = extract(soup = soup1, df_new = df_new)
df_new = extract(soup = soup2, df_new = df_new)
