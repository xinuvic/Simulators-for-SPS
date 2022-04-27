# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:16:48 2021
@author: XIN

Input: 
i: vehicle ID
ResList: Resource selection list for all vehicles
VehicleNum: Number of vehicles
VehicleLocation: Location distribution of all vehicles
Power: Transmit power

Output:
Distribution of received power strength on all resouces
"""

from Distance import Distance

def RSRP(i,ResList,ResNum,VehicleNum,VehicleLocation,Power):
    a=[]
    RSRPDistribution = [0]*ResNum        
    for j in range(0,VehicleNum):
        #print(ResList[j])
        if ResList[j]==a:
            continue
        k = ResList[j]
        if i==j:
            continue
        RSRPValue = Power*Distance(i,j,VehicleLocation)**(-3.68)
        if RSRPDistribution[k] == 0:
            RSRPDistribution[k] = RSRPValue
        else:
            RSRPDistribution[k] += RSRPValue
    return RSRPDistribution    
