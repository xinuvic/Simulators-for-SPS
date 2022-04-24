# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:15:25 2021
@author: XIN
Input: 
i: Transmitter ID
j: Another transmitter ID
R: Resource selection list for all vehicles

Output:
Whether i and j select the same resources, 1--Yes, 0--No
"""
def ResCollisionCheck(i,j,R):
    if R[i] == R[j] :
        Same = 1
    else:
        Same = 0
    return Same
