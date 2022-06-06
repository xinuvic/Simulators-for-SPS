# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:48:14 2022

@author: CSUST
"""

import pandas as pd
import csv
import numpy as np


set_of_staying_nodes=[]# The list "set_of_staying_nodes" is used for recording the IDs of vehicles who keep staying in the map

vehicle_data=[] 
for s in range(1,151):
    step_number=170+s
    location_step=pd.read_csv("data\\selected_part_cologne_positions_%s.csv"%str(step_number),header=None)
    vehicle_data.append(location_step)
    if s==1:  # list all vehicle IDs at first time-step
        set_of_staying_nodes=list(vehicle_data[0][0])
    else:  # check those non-repeated ones and delete them
        for g in set_of_staying_nodes:
            if g not in list(vehicle_data[s-1][0]):
                set_of_staying_nodes.remove(g) # <-- delete non-repeated one
        # index of vehicles
        
vehicle_num = len(set_of_staying_nodes)   

set_of_platoon=[] # ID set of platoon vehicles
set_of_non_platoon=[] # ID set of non-platoon vehicles
for platoon_index_find in range(0,len(set_of_staying_nodes)):
    if set_of_staying_nodes[platoon_index_find]>1000: # since the ID of platoon vehicles is larger than 1000
        set_of_platoon.append(platoon_index_find)
    else:
        set_of_non_platoon.append(platoon_index_find)
  
           
observe_vehicles_mix=[]
for s in range(0,150):
    for i in range(0,len(vehicle_data[s][0])):
        if vehicle_data[s][0][i] in set_of_staying_nodes:
            observe_vehicles_mix.append([vehicle_data[s][1][i],vehicle_data[s][2][i]]) # save locations of all vehicles
            


# save the locations, platoon IDs and non-platoon IDs, respectively
filename='realmap_vehicle_location'
n=0

f=open('%s.csv'%filename,'w',newline='')
writer=csv.writer(f)
for i in observe_vehicles_mix:
    writer.writerow(i)
f.close()

filename='set_of_platoon'
n=0
f=open('%s.csv'%filename,'w',newline='')
writer=csv.writer(f)
writer.writerow(set_of_platoon)
f.close()


filename='set_of_non_platoon'
n=0
f=open('%s.csv'%filename,'w',newline='')
writer=csv.writer(f)
writer.writerow(set_of_non_platoon)
f.close()


# =============================================================================
# to read the saved csv file, using the following codes
# =============================================================================
# observe_vehicles = [[] for i in range(0,150)] # 150 is the whole sampling time duration
# data_all=np.array(pd.read_csv("realmap_vehicle_location.csv",header=None)).tolist()
# vehicle_num=int(len(data_all)/150)
# for i in range(0,150):
#     observe_vehicles[i]=data_all[int(i*vehicle_num):int((i+1)*vehicle_num)] # export vehicle locations every timestep
    
# set_of_platoon=np.array(pd.read_csv("set_of_platoon.csv",header=None)).tolist()[0]
# set_of_non_platoon=np.array(pd.read_csv("set_of_non_platoon.csv",header=None)).tolist()[0]
