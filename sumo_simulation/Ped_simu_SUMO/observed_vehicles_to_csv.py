# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 14:48:14 2021

@author: xin
"""

import pandas as pd
import csv



set_of_staying_nodes=[]

vehicle_data=[] 
for s in range(1,401):
    step_number=100+s
    location_step=pd.read_csv("Data_ped\\location_for_timestep%s.csv"%str(step_number),header=None)
    vehicle_data.append(location_step)
    if s==1:  # list all vehicle IDs at first time-step
        set_of_staying_nodes=list(vehicle_data[0][0])
    else:  # check those non-repeated ones and delete them
        for g in set_of_staying_nodes:
            if g not in list(vehicle_data[s-1][0]):
                set_of_staying_nodes.remove(g) 
        
vehicle_num = len(set_of_staying_nodes)   

  
# =============================================================================
# using observe_vehicles as a list to record all locations          
# =============================================================================
observe_vehicles=[]
for s in range(0,200):
    for i in range(0,len(vehicle_data[s][0])):
        if vehicle_data[s][0][i] in set_of_staying_nodes:
            observe_vehicles.append([s,vehicle_data[s][1][i],vehicle_data[s][2][i],vehicle_data[s][0][i]]) # save locations of all vehicles
            

# =============================================================================
# save the locations of all vehicles during a given time period
# =============================================================================
filename='sumo_vehicle_location'
n=0

f=open('%s.csv'%filename,'w',newline='')
writer=csv.writer(f)
for i in observe_vehicles:
    writer.writerow(i)
f.close()

