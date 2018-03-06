#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 20:21:30 2018

@author: Kieran
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
products = []
import datetime

import time

for i in range(1,51):
    response = requests.get('https://www.gumtree.com/search?search_category=mobile-phones&search_location=uk&q=phone&page={}'.format(i))
    respTxt = response.text
    print('getting page {}'.format(i))
    time.sleep(4)
    point1 = respTxt.find('<section class="grid-container space-pts">')
    point2 = respTxt.find('<span data-l1-category="true" class="hide-fully">Stuff for Sale</span>')

    filterTxt = respTxt[point1:point2]
    parsed_html = BeautifulSoup(filterTxt, 'html.parser')
    for art in parsed_html.find_all('article'):
        titles = art.find_all("h2", class_="listing-title")
        prices = art.find_all(attrs={"itemprop": "price"})
        link = art.find_all('a', class_='listing-link')
        if(len(prices) == 1):
            products.append([prices[0]['content'], titles[0].text, link[0]['href']])

my_df = pd.DataFrame(products)

import glob

all_files = glob.glob("Data/out*.csv")     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f, header=None) for f in all_files)
dataset   = pd.concat(df_from_each_file, ignore_index=True)
#toWrite = my_df[~my_df.index.isin(dataset.index)]
merge = my_df.merge(dataset.drop_duplicates(), on=[2], 
                   how='left', indicator=True)
toWrite = merge.loc[merge['_merge'] == 'left_only'].iloc[:,:3]
if (len(toWrite) > 0):
    toWrite.to_csv('Data/out{}.csv'.format(str(datetime.datetime.now())), index=False, header=False)


