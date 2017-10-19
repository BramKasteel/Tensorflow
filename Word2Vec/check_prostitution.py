#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 12:14:23 2017

@author: bram

Opens excel, and checks each entry in first column for
string 'prostitutie' or for code '82PROS'

Saves relevant cells to pickle object

Also performs some string manipulation to find out if the text is actually relevant
This by bag-of-words search
"""

from xlrd import open_workbook
import pickle
import collections
import math
import pandas as pd
from collections import Counter

filename = 'toyData.xlsx'

wb = open_workbook(filename)

bigList = []
bigListClean =[]
bigString = ''
s = wb.sheets()[0]
for row in range(0,s.nrows):
    value = (s.cell(row,0).value)
    #if it contains the word 'prostitutie' or '82PROS', we will append
    if ('prostitutie' in value.lower()) or ('82pros' in value.lower()):
        ##value = value.decode('utf-8', 'ignore') #Look into 'replace' for improvement DOES NOT DO ANYTHING
        bigList.append(value)        
        
        #Clean up value
        value = value.replace('\t',' ')
        # Replace enters
        value = value.replace('\n',' ')
        # Replace periods
        value = value.replace('. ',' ')
        # Commas
        value = value.replace(', ',' ')
        # Etc
        value = value.replace(': ',' ')
        value = value.replace('; ',' ')
        value = value.replace('(',' ')
        value = value.replace(')',' ')
        value = value.replace('"',' ')
        value = value.replace('-',' ')
        # Make lowercase
        value = value.lower()
        
        while value.count('  ')>0:
            value = value.replace('  ',' ')
        bigListClean.append(value)
        
        #First convert to utf-8
        bigString += value

#Save the three big list with pickle
with open('toyDataList.pickle','wb') as f:
    pickle.dump([bigList,bigListClean,bigString], f)

del bigList
del bigListClean
del bigString

with open('toyDataList.pickle','rb') as f:
    _,bigListClean,_ = pickle.load(f)

### Try to match some strings or parts of sentences with keywords
### And use the words in these strings to find other keywords (TF-IDF)
#word count for all strings
longString = ' '.join(bigListClean)
words = longString.split(' ')
Nwords = len(words)

tf = collections.Counter(words).most_common(50000)
tf = pd.DataFrame(tf, columns=['word','count'])
tf = tf[tf['count']>25]
freqTotal = (tf['count']+1)/Nwords
tf = tf.assign(freqTotal = freqTotal)
tf = pd.DataFrame(tf,columns=['word','count','freqTotal'])
#idf = []
#for counter in range(tf.shape[0]):
#    if (counter%1000)==0:
#        print(counter)
#    word = tf.iloc[counter,0]
#    idf.append((len(bigListClean)/(sum(word in document for document in bigListClean)),))

#Convert to data frames
#idf = pd.DataFrame(idf, columns = ['idf'])
#tfidf = tf
#newcol = idf['idf']
#tfidf.assign(idf= newcol)

#Save intermediate results
#with open('tfidf.pickle','wb') as f:
#    pickle.dump([tf],f)

#with open('tfidf.pickle','rb') as f:
#    tf = pickle.load(f)

dwangList = []
for item in bigListClean:
    if (any(word in item for word in ['dwang','gedwongen'])):
        dwangList.append(item)

def wordFreq(documentList,wordList):
    longString = ' '.join(documentList)
    words = longString.split(' ')
    Nwords = len(words)
    #relFreq = pd.DataFrame(wordList, columns = ['word'])
    #relFreq.assign(relfreq = wordList)
    #for word in wordList:
    
    count = collections.Counter(words).most_common(50000)
    count = pd.DataFrame(count,columns=['word','count']) 
    count = count.assign(relFreq = (count['count']+1)/Nwords)
    count = pd.DataFrame(count,columns=['word','count','relFreq'])
    return count

relcount = wordFreq(dwangList,tf['word'])

#Only once, for this example. Merge the two dataframes, and sort for highest log(freq/freq)
test = tf.merge(relcount, left_on='word',right_on='word',how='inner')
quotient = test['relFreq']/test['freqTotal']
test = test.assign(quotient = quotient)
test = pd.DataFrame(test,columns = ['word','count_x','freqTotal','count_y','relFreq','quotient'])
test0 = test.sort_values('quotient')

#### -->> aantal documenten waarin het woord wordt gevonden moet ook groter wezen dan 1 natuurlijk!    
