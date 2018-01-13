# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:30:49 2018

@author: Kevin
"""

from bs4 import BeautifulSoup
import requests
import csv
import datetime

"""
Red wine url: 
    Category: Red wine (to exclude rose)
    Rating 4, 4.5 or 5. 
    Dan Murphy's (not Connections). 
    Price 5 - 30.
"""
source = requests.get('https://www.danmurphys.com.au/dm/navigation/navigation'
                      '_results_gallery.jsp?params=fh_location%3D%2F%2Fcatalo'
                      'g01%2Fen_AU%2Fcategories%3C%7Bcatalog01_25343743020259'
                      '14%7D%2F5.0%3Cprice%3C30.0%2Fwebmaincategory%3E%7Bred2'
                      '0wine%7D%2Fweb_dsv_flag%3E%7Bdan20murphy27s%7D%2Fbv_cu'
                      'stomer_ratings%3E%7B40%3B45%3B50%7D%26fh_view_size%3D1'
                      '20%26fh_sort%3D-sales_value_30_days%26fh_modification%'
                      '3D%2528secondid%253C%257Bdm_b999999000632%257D%252Cblo'
                      'cked%2529%252C%2528secondid%253C%257Bdm_mystery57%257D'
                      '%252Cblocked%2529%252C%2528secondid%253C%257Bdm_myster'
                      'y52%257D%252Cblocked%2529%252C%2528secondid%253C%257Bd'
                      'm_757646%257D%252Cblocked%2529%252C%2528secondid%253C%'
                      '257Bdm_610528%257D%252Cblocked%2529%252C%2528secondid%'
                      '253C%257Bdm_786481%257D%252Cblocked%2529%252C%2528seco'
                      'ndid%253C%257Bdm_616722%257D%252Cblocked%2529%252C%252'
                      '8instock%253D0%252Cbottom%2529&resetnav=false&storeExc'
                      'lusivePage=false').text

soup = BeautifulSoup(source, 'lxml')

# "today" is the col name of the new col to be added to the existing df.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

csv_file = open('{}.csv'.format(today), 'w', newline = '') 

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['product_name', today])

for product in soup.find_all('div', {'class':'independent-product-module'}):
    product_name = product.div.h2.a['title']
    # Replace Frech letters with English
    translationTable = str.maketrans("éàèùâêîôóûç", "eaeuaeioouc")
    product_name = product_name.translate(translationTable)
    try:
        price = product.find_all('li', {'class':'price-secondary'})[0]\
                .p.span.text
    except IndexError:
        price = product.find_all('span',{'class':'price'})[0].text
    price = price.replace('$','')
    csv_writer.writerow([product_name, price])
    
csv_file.close()
    
    
    
    
    
    
    