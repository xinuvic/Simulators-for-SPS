# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:11:05 2021
@author: XIN
Input: a list
Outout: list with rows converted into columns 
"""
def ConvertRowsintoColumns(Alist):
    newlist=[[row[i] for row in Alist] for i in range(len(Alist[0]))]
    return newlist
