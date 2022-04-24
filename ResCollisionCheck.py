# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:15:25 2021
@author: XIN
"""
def ResCollisionCheck(i,j,R):
    if R[i] == R[j] :
        Same = 1
    else:
        Same = 0
    return Same