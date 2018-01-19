# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:30:49 2018

@author: Kevin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

"""
Red wine url: 
    Category: Red wine (to exclude rose)
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
                       '25914%7D%2F5.0%3Cprice%3C30.0%2Fwebmaincategory%3E%7B'
                       'red20wine%7D%2Fweb_dsv_flag%3E%7Bdan20murphy27s%7D%26'
                       'fh_view_size%3D120%26fh_sort%3D-sales_value_30_days%2'
                       '6fh_modification%3D%2528secondid%253C%257Bdm_b9999990'
                       '00632%257D%252Cblocked%2529%252C%2528secondid%253C%25'
                       '7Bdm_mystery57%257D%252Cblocked%2529%252C%2528secondi'
                       'd%253C%257Bdm_mystery52%257D%252Cblocked%2529%252C%25'
                       '28secondid%253C%257Bdm_757646%257D%252Cblocked%2529%2'
                       '52C%2528secondid%253C%257Bdm_610528%257D%252Cblocked%'
                       '2529%252C%2528secondid%253C%257Bdm_786481%257D%252Cbl'
                       'ocked%2529%252C%2528secondid%253C%257Bdm_616722%257D%'
                       '252Cblocked%2529%252C%2528instock%253D0%252Cbottom%25'
                       '29%26fh_maxdisplaynrvalues_categories%3D-1&resetnav=f'
                       'alse&storeExclusivePage=false').text

source2 = requests.get('https://www.danmurphys.com.au/dm/navigation/navigatio'
                       'n_results_gallery.jsp?params=fh_location%3D%2F%2Fcata'
                       'log01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020'
                       '25914%7D%2F5.0%3Cprice%3C30.0%2Fwebmaincategory%3E%7B'
                       'red20wine%7D%2Fweb_dsv_flag%3E%7Bdan20murphy27s%7D%26'
                       'fh_view_size%3D120%26fh_start_index%3D120%26fh_sort%3'
                       'D-sales_value_30_days%26fh_modification%3D%2528second'
                       'id%253C%257Bdm_b999999000632%257D%252Cblocked%2529%25'
                       '2C%2528secondid%253C%257Bdm_mystery57%257D%252Cblocke'
                       'd%2529%252C%2528secondid%253C%257Bdm_mystery52%257D%2'
                       '52Cblocked%2529%252C%2528secondid%253C%257Bdm_757646%'
                       '257D%252Cblocked%2529%252C%2528secondid%253C%257Bdm_6'
                       '10528%257D%252Cblocked%2529%252C%2528secondid%253C%25'
                       '7Bdm_786481%257D%252Cblocked%2529%252C%2528secondid%2'
                       '53C%257Bdm_616722%257D%252Cblocked%2529%252C%2528inst'
                       'ock%253D0%252Cbottom%2529%26fh_maxdisplaynrvalues_cat'
                       'egories%3D-1&resetnav=false&mfRefsh=false&storeExclus'
                       'ivePage=false').text
                       
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
    
    
    
    
    