# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:13:46 2021
@author: XIN
Input:
i: Transmitter ID
j: Receiver ID
R: Resource selection list for all vehicles
VehicleNum: Number of vehicles
VehicleLocation: Location distribution of all vehicles
Power: Transmit Power
"""

from ResCollisionCheck import ResCollisionCheck
from Distance import Distance
import numpy as np

def CalculateSINR(i,j,R,VehicleNum,VehicleLocation,Power):
    Interference=0
    for s in range(0,VehicleNum):
        if True:
        #if Distance(s,j,VehicleLocation)<dint:
            if s == i or s == j:
                continue
            else:
                if ResCollisionCheck(i,s,R) == 1:
                    #same = 1
                    Interference += Power*Distance(s,j,VehicleLocation)**(-3.68)
    SINR = 10*np.log10((Power*Distance(i,j,VehicleLocation)**(-3.68))/(Interference+10**(-6.46)))
    return SINR
