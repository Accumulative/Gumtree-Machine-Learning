#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 19:06:21 2018

@author: Kieran
"""
import string
import pandas as pd
import numpy as np
import glob

all_files = glob.glob("out*.csv")     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f, header=None) for f in all_files)
wholeset   = pd.concat(df_from_each_file, ignore_index=True)
cut = int(len(wholeset) * 0.8)
dataset = wholeset[:cut]
testset = wholeset[cut+1:]

common = ['and','or','for','to','with','the','from','in','but','not','an','only','any','on','of','a']
neutral = ['phone']

def strip_word(element):
    element = element.replace("\n",'').lower()
    if element[-1] == 's':
        element = element[:-1]
    element = element.translate(str.maketrans({key: None for key in string.punctuation}))
    
    return element

def find_element_in_list(element, list_element):
    
    for i in range(0, len(list_element)):
        if list_element[i][0] == strip_word(element):
            return i
    return None

all_terms = []
for product in dataset.values:
    for word in product[1].split(" "):
        if word not in common and word not in neutral:
            index = find_element_in_list(word, all_terms)
            if index is None:
                toStore = strip_word(word)
                if toStore != "":
                    all_terms.append([toStore, 1, float(product[0]), 0])
            else:
                if float(product[0]) < 1000 and float(product[0]) > 0:
                    all_terms[index][1] += 1
                    all_terms[index][2] += float(product[0])
all_terms.sort(key=lambda x:-x[1])

for terms in all_terms:
    terms[3] = terms[2]/terms[1]
    
def guess_price(product):
    cost = 0
    num = 0
    wordsDone = []
    for word in product.split(" "):
        index = find_element_in_list(word, all_terms)
        if word not in wordsDone:
            wordsDone.append(word)
            if index is not None:
                cost += all_terms[index][3]
                num += 1
#                print(word, all_terms[index][3])
    if num != 0:
        return cost / num
    return 0
plotdata = [x for x in all_terms if x[1] > 10][1:50]
import matplotlib.pyplot as plt
plt.bar(np.arange(len(plotdata)),[x[1] for x in plotdata])
plt.xticks(np.arange(len(plotdata)),[x[0] for x in plotdata],rotation=90);
plt.title('Histogram of ads selections')
plt.xlabel('Ads')
plt.ylabel('Number of times each ad was selected')
plt.show()

diffence = []
for product in testset.values:
#    print(product[1], product[0], guess_price(product[1]))
    if product[0] != 0:
        diffence.append((guess_price(product[1]) - product[0])/product[0])
    else:
        diffence.append(10000)
    
diffenceval = [1  if (float(a) < 0.2 and float(a)> -0.2) else 0 for a in diffence]

print(sum(diffenceval)/len(diffenceval))