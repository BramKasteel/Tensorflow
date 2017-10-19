#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:29:12 2017

@author: bram

Make sure the textdata is saved as utf-8.
"""

import sys
import codecs

filename = 'toyData.txt'
output1 = 'lines.txt'

#Read file line-by-line, and keep if it does not start with a tab or space
with open(filename, "r") as f:
    for line in f:
        if not(line[0] in '\t \n'):
            print(line)
            

        


# Replace tabs
file_str = file_str.replace('\t',' ')

# Replace enters
file_str = file_str.replace('\n',' ')

# Replace periods
file_str = file_str.replace('. ',' ')

# Commas
file_str = file_str.replace(', ',' ')

# Etc
file_str = file_str.replace(': ',' ')
file_str = file_str.replace('; ',' ')
file_str = file_str.replace('(',' ')
file_str = file_str.replace(')',' ')
file_str = file_str.replace('"',' ')
file_str = file_str.replace('-',' ')

# Make lowercase
file_str = file_str.lower()

while file_str.count('  ')>0:
    file_str = file_str.replace('  ',' ')

filename = 'toyDataClean.txt'
with open(filename, "w") as f:
    f.write(file_str)