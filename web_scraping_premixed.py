# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 18:52:53 2018

@author: Kevin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

"""

# IGNORE THIS CHUNK SINCE PREMIXED DRINKS UNDER WHISKY TAB ARE DUPLICATES

#Whisky based premixed url (source1): 
#    Category: premix drink (to exclude Whisky)
#    Product 1 to 120.

# IGNORE ENDS


# Only focus on the "spirit" tab since all the premix (including Whisky based)
# are presented under this tab.

Other Spirit based premixed url:
    Category: premix drink (to exclude spirit)
    Dan Murphy's (not Connections). 
    Product 1 to 120. Then 121 to 240.
    
"""

# "today" is the col name of the new col to be added to the existing df.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

df_new = pd.DataFrame(columns = [today])

source1 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '85866%7D%2Fwebmaincategory%3E%7Bpremix20drinks%7D%2Fw'
                       'eb_dsv_flag%3E%7Bdan20murphy27s%7D%26fh_view_size%3D1'
                       '20%26fh_sort%3D-sales_value_30_days%26fh_modification'
                       '%3D%2528secondid%253C%257Bdm_b999999000632%257D%252Cb'
                       'locked%2529%252C%2528secondid%253C%257Bdm_mystery57%2'
                       '57D%252Cblocked%2529%252C%2528secondid%253C%257Bdm_my'
                       'stery52%257D%252Cblocked%2529%252C%2528secondid%253C%'
                       '257Bdm_757646%257D%252Cblocked%2529%252C%2528secondid'
                       '%253C%257Bdm_610528%257D%252Cblocked%2529%252C%2528se'
                       'condid%253C%257Bdm_786481%257D%252Cblocked%2529%252C%'
                       '2528secondid%253C%257Bdm_616722%257D%252Cblocked%2529'
                       '%252C%2528instock%253D0%252Cbottom%2529%26fh_maxdispl'
                       'aynrvalues_categories%3D-1&resetnav=false&storeExclus'
                       'ivePage=false').text

source2 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '85866%7D%2Fwebmaincategory%3E%7Bpremix20drinks%7D%2Fw'
                       'eb_dsv_flag%3E%7Bdan20murphy27s%7D%26fh_view_size%3D1'
                       '20%26fh_start_index%3D120%26fh_sort%3D-sales_value_30'
                       '_days%26fh_modification%3D%2528secondid%253C%257Bdm_b'
                       '999999000632%257D%252Cblocked%2529%252C%2528secondid%'
                       '253C%257Bdm_mystery57%257D%252Cblocked%2529%252C%2528'
                       'secondid%253C%257Bdm_mystery52%257D%252Cblocked%2529%'
                       '252C%2528secondid%253C%257Bdm_757646%257D%252Cblocked'
                       '%2529%252C%2528secondid%253C%257Bdm_610528%257D%252Cb'
                       'locked%2529%252C%2528secondid%253C%257Bdm_786481%257D'
                       '%252Cblocked%2529%252C%2528secondid%253C%257Bdm_61672'
                       '2%257D%252Cblocked%2529%252C%2528instock%253D0%252Cbo'
                       'ttom%2529%26fh_maxdisplaynrvalues_categories%3D-1&res'
                       'etnav=false&mfRefsh=false&storeExclusivePage=false'
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