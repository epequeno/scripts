# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 16:30:05 2014

@author: Estevan Adrian Pequeno
"""

for i in range(1, 1001):
    file_name = str(i) + ".txt"
    fh = open(file_name, 'w')
    fh.close()
    
