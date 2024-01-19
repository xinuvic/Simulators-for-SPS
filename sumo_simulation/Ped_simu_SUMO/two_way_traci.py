# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:23:54 2022

@author: xin
"""


import os, sys
import traci
import numpy as np
import csv


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
# =============================================================================
# change the path based on your configuration
# =============================================================================
sumoBinary = r"C:\Program Files (x86)\DLR\Sumo\bin\sumo-gui.exe" # updating the SUMO path
sumoCmd = [sumoBinary, "-c", "ETSI_TR_138_913_V14_3_0_urban.sumocfg"]

    

def vehicle_information():
    step = 0
    a = 0
    index = 0
    x_coordinate = np.array([])
    y_coordinate = np.array([])
    
    while step < 1000: 
       location_list=[]
       traci.simulationStep()

       #vehicles parser
       for vehicleId in traci.vehicle.getIDList():
           x, y = traci.vehicle.getPosition(vehicleId)           
           x_coordinate = round(x,2)
           y_coordinate = round(y,2)
           type = traci.vehicle.getTypeID(vehicleId) 
           location_list.append([vehicleId,x_coordinate,y_coordinate,type]) # saving three items in each line
           index +=1  

       #person parser
       for personId in traci.person.getIDList():
           x, y = traci.person.getPosition(personId)           
           x_coordinate = round(x,2)
           y_coordinate = round(y,2)
           type = traci.person.getTypeID(personId)
           location_list.append([personId,x_coordinate,y_coordinate,type]) # saving three items in each line
           index +=1         


       if 100<step<=500: # sampling time duration
           filename_locations='Data_ped\\location_for_timestep'+str(step) # each csv-file for each step
           f = open('%s.csv'%filename_locations,'w',newline='')
           writer = csv.writer(f)
           for i in location_list:
               writer.writerow(i)
           f.close()
       
       vehicle_number = len(traci.vehicle.getIDList())
       print('step',step,"Total number of vehicles: " + str(vehicle_number))
       print()
       
       person_number = len(traci.person.getIDList())
       print('step',step,"Total number of person: " + str(person_number))
       print()

       a += 1             
       step += 1
       index = 0
       x_coordinate = np.array([])
       y_coordinate = np.array([])
 
def main():    
    traci.start(sumoCmd)
    vehicle_information()
    traci.close()

       
if __name__ == "__main__":
    main()
    

