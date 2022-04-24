# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:09:36 2021
@author: XIN
Input: the list indicating collision/success for channel access
timespot: timespot of resource selection for one vehicle
SimulationTime: Total duration of simulation
BeaconRate: Beacon rate
RC: RC range
StartTime: the starting point for simulation result recording
maximalTime: Maximal tolerable time of access failure

Output:
CountSuccess,CountFail,collision,s
"""

def CountConsecutiveNumber(Alist,number,timespot,SimulationTime,BeaconRate,RC,StartTime,maximalTime):

    CountSuccess=0
    CountFail=0
    collision=0
    s=0
    for t in timespot:
        t=t-StartTime
        for j in range(0,len(Alist)):
            s+=1
            if Alist[j][t]==0:
                CountSuccess+=1
            else:
                collision+=1
                if t<=SimulationTime-BeaconRate:
                    if sum(Alist[j][t:int(t+maximalTime)])>=maximalTime: 
                        CountFail+=1
                    else:
                        CountSuccess+=1
    return CountSuccess,CountFail,collision,s
