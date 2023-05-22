# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 19:52:14 2022

@author: xin
"""
class RBG():
    def __init__(self,timeslot,subchannel):
        self.timeslot = timeslot
        self.subchannel = subchannel
        
        
    def RBG_vehicle_mapping(self,vehicle_list,vehicle):
        self.vehicle_list.append(vehicle)
    
    def generate_RBGs(num_slot,num_subch):
        RBG_intance_list = []
        for i in range(num_slot):
            RBG_intance_each_slot = []
            for j in range(num_subch):
                RBG_intance_each_slot.append(RBG(i,j))
            RBG_intance_list.append(RBG_intance_each_slot)    

class RGBs_set():
    def __init__(self,timeslot,subchannel):
        self.timeslot = timeslot
        self.subchannel = subchannel