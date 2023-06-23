# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 19:49:51 2022

@author: xin
"""
from RBG import RBG


class Message():
    def __init__(self,mtype,mdelay,mgeneration_time,mserved_RBG,mID):
        self.mID = mID
        self.mtype = mtype
        self.mdelay = mdelay
        self.mgeneration_time = mgeneration_time
        self.mserved_RBG = mserved_RBG
        
    def serve_RBG(self,timeslot,subchannel):
        self.mserved_RBG = RBG(timeslot,subchannel)

    def set_sensing_window(self,sensing_duration):
        self.sensing_duration = sensing_duration
        self.sensing_window = [self.mgeneration_time-self.sensing_duration,self.mgeneration_time]

         
class Beacon(Message):
    def __init__(self,mtype,mdelay,mgeneration_time,mserved_RBG,rate,mID):
        super().__init__(mtype,mdelay,mgeneration_time,mserved_RBG,mID)
        self.rate = rate
        self.interval = 1000*(1/self.rate)
        
    def set_selection_window(self,selection_window):
        self.selection_window = [self.mgeneration_time,self.mgeneration_time+self.interval]

class Emergency(Message):
    def __init__(self,mtype,mdelay,mgeneration_time,mserved_RBG,lamda,num_RBG,mID):
        super().__init__(mtype,mdelay,mgeneration_time,mserved_RBG,mID)
        self.lamda = lamda
        self.num_RBG = num_RBG
        #self.interval = np.random.exponential(scale=self.lamda)
        
    def set_lamda(self,lamda):
        self.lamda = lamda
        
    def set_mgeneration_time(self,mgeneration_time):
        self.mgeneration_time = mgeneration_time
        
    def set_interval(self,interval):
        self.interval = interval

    def set_selection_window(self,selection_window):
        self.selection_window = [self.mgeneration_time,self.mgeneration_time+self.mdelay]


    