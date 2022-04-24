# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:13:05 2021
@author: XIN
"""
import math
def Distance(i,j,VehicleLocation):
    distance = math.sqrt((VehicleLocation[i][0]-VehicleLocation[j][0])**2 + (VehicleLocation[i][1]-VehicleLocation[j][1])**2)
    return distance
