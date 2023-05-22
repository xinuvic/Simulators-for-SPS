# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 10:28:49 2022

@author: xin
"""
import RBG

class Channel():
    def __init__(self, num_subch, interval):
        self.num_subch = num_subch
        self.RBs_in_new_slot = []
        self.interval = interval
        self.num_RBGs_in_one_RRI = int(num_subch*interval)
        
        
    def create_new_RBGs(self,num_subch,timeslot):
        self.RBGs_in_new_slot = []
        for i in range(num_subch):
            RB = RBG(timeslot,i)
            self.RBGs_in_new_slot.append(RB)
            
        