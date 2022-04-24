# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:18:48 2021
@author: XIN

Input: 
VehicleNum: Number of vehicles
ResNum: Number of resources

Output: random resource selection
"""
import random
def ResSelectionInitial(VehicleNum,ResNum):
    ResSelection = [[]]*VehicleNum
    for i in range(0,VehicleNum):
        ResSelection[i] = random.randint(0,ResNum-1)
    return ResSelection
