# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:11:05 2021
@author: XIN
"""
def ChangeRowandColumn(originallist):
    newlist=[[row[i] for row in originallist] for i in range(len(originallist[0]))]
    return newlist