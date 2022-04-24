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
CountSucceed,CountFail,collision,s
"""

def CountConsecutiveNumber(Alist,number,timespot,SimulationTime,BeaconRate,RC,StartTime,maximalTime):

    CountSucceed=0
    CountFail=0
    collision=0
    s=0
    for t in timespot:
        t=t-StartTime
        for j in range(0,len(Alist)):
            s+=1
            if Alist[j][t]==0:
                CountSucceed+=1
            else:
                collision+=1
            # if RC set for last resource selection is no less than 20, regard it as collision
                if t<=SimulationTime-BeaconRate:
                    if sum(Alist[j][t:int(t+maximalTime)])>=maximalTime: 
                        CountFail+=1
                    else:
                        CountSucceed+=1
    return CountSucceed,CountFail,collision,s
