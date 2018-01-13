# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv
from urllib.request import urlopen
from lxml import html
import time 
import re
import datetime

# "today" is the col name of the new col to be added to the existing df.
now = datetime.datetime.now()
today = str(now.strftime("%Y-%m-%d"))

browser = webdriver.Chrome() # chromedriver.exe need to be in the same folder
url = 'http://boozle.com.au/browse/s/t:Wine'
browser.get(url)

# Wait for page to load. Consider using WebDriverWait
# https://coderwall.com/p/vivfza/fetch-dynamic-web-pages-with-selenium
time.sleep(30)

html_page = browser.page_source

# These lines are from Stanford webpages, but other ways also work.
##returns the inner HTML as a string
#innerHTML = browser.execute_script("return document.body.innerHTML") 
#
##parse innerHTML
#page = html.document_fromstring(innerHTML)
#
#products_list = page.get_element_by_id("products-list") #get the fieldset
#
#products_list_text = products_list.text_content()
#
##print(products_list_text)

browser.quit()

soup = BeautifulSoup(html_page, "lxml")

# Maybe to wrap w/ context mngr
csv_file = open('{}.csv'.format(today), 'w', newline = '') 

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['product_name', today])

for product in soup.find_all('div', class_= 'price-info'):
    product_name = product.find('h3', itemprop='name').text
    low_price = product.find('span', itemprop='lowPrice').text
    # Now delete "$"
    regex = re.compile("[$]")
    low_price = regex.sub("", low_price)
    csv_writer.writerow([product_name, low_price])

csv_file.close()

