# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:28:30 2018

@author: Kevin
"""


from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

"""
Sparkling url: 
    Dan Murphy's (not Connections). 
    Price: 1 to 100.
    Product 1 to 120.
"""

# "today" is the col name of the new col to be added to the existing df.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

df_new = pd.DataFrame(columns = [today])

source = requests.get('https://www.danmurphys.com.au/dm/navigation/navigation'
                      '_results_gallery.jsp?params=fh_location%3D%2F%2Fcatalo'
                      'g01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020260'
                      '62%7D%2F1.0%3Cprice%3C100.0%2Fweb_dsv_flag%3E%7Bdan20m'
                      'urphy27s%7D%26fh_view_size%3D120%26fh_sort%3D-sales_va'
                      'lue_30_days%26fh_modification%3D%2528secondid%253C%257'
                      'Bdm_b999999000632%257D%252Cblocked%2529%252C%2528secon'
                      'did%253C%257Bdm_mystery57%257D%252Cblocked%2529%252C%2'
                      '528secondid%253C%257Bdm_mystery52%257D%252Cblocked%252'
                      '9%252C%2528secondid%253C%257Bdm_757646%257D%252Cblocke'
                      'd%2529%252C%2528secondid%253C%257Bdm_610528%257D%252Cb'
                      'locked%2529%252C%2528secondid%253C%257Bdm_786481%257D%'
                      '252Cblocked%2529%252C%2528secondid%253C%257Bdm_616722%'
                      '257D%252Cblocked%2529%252C%2528instock%253D0%252Cbotto'
                      'm%2529%26fh_maxdisplaynrvalues_categories%3D-1&resetna'
                      'v=false&storeExclusivePage=false').text
                       
soup = BeautifulSoup(source, 'lxml')

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

df_new = extract(soup = soup, df_new = df_new)
