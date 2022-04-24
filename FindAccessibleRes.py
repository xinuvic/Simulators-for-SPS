#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:17:46 2021
@author: XIN
Input:
i: Vehicle ID
AverageRSSI: RSSI distribution detected by vehicle i.
ResList: Resource selection list for all vehicles
ResNum: Total number of Resources
AccessibleResRatio: Ratio of accessible resources and all resources within a selection window
Output:
Least a% interferred resources, a% is given with AccessibleResRatio
"""
import numpy as np

def FindAccessibleRes(i,AverageRSSI,ResList,ResNum,AccessibleResRatio):
    num_need = int(AccessibleResRatio * ResNum)
    temp=[]
    w=[]
    Inf = 1000
    p = AverageRSSI
    q = p[:]
    s = min(p)
    #print('s:',s)
    for kkk in range(0,ResNum):  
        w.append(q.index(s))
        q[q.index(s)]=Inf
        if s not in q:
            break
    if len(w)>num_need:
        temp = np.random.choice(w,size = num_need,replace = False)
    else:
        for sss in range(0,num_need):
            temp.append(p.index(min(p)))
            p[p.index(min(p))]=Inf # exclude the recorded maximum number
    return temp  
