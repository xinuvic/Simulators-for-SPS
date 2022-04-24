# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:16:48 2021
@author: XIN
"""
from Distance import Distance

def RSSI(i,ResList,ResNum,VehicleNum,VehicleLocation,Power):
    a=[]
    RSSIDistribution = [0]*ResNum        
    for j in range(0,VehicleNum):
        #print(ResList[j])
        if ResList[j]==a:
            continue
        k = ResList[j]
        if i==j:
            continue
        RSSIValue = Power*Distance(i,j,VehicleLocation)**(-3.68)
        if RSSIDistribution[k] == 0:
            RSSIDistribution[k] = RSSIValue
        else:
            RSSIDistribution[k] += RSSIValue
    return RSSIDistribution    