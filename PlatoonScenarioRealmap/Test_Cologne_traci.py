# -*- coding: utf-8 -*-
"""
Created on Wed May 18 11:51:50 2022

@author: kevin
"""

import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
    

sumoBinary = r"D:\Eclipse\Sumo\bin\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "selected_part_cologne.sumocfg"]

import traci
import numpy as np
import math
import simpla
import csv

def calculate_distance(x_coordinate, y_coordinate, car1, car2):
    distance = math.sqrt((x_coordinate[car1] - x_coordinate[car2])**2 + 
                         (y_coordinate[car1] - y_coordinate[car2])**2)
    print("distance between car number " + str(car1) + " and car number " 
          + str(car2) + " is " + str(distance) + "m")
    
    
def vehicle_information():
    step = 0
    a = 0
    index = 0
    x_coordinate = np.array([])
    y_coordinate = np.array([])
    
    
    while step < 2000: 
       location_list=[]
       traci.simulationStep()
       for vehicleId in traci.vehicle.getIDList():
           #list = traci.vehicle.getIDList();           
           #speed = traci.vehicle.getSpeed(vehicleId)
           x, y = traci.vehicle.getPosition(vehicleId)           
           x_coordinate = round(x,2)
           y_coordinate = round(y,2)
           location_list.append([vehicleId,x_coordinate,y_coordinate]) # saving three items in each line
           index +=1       
       if 300<step<=500: # sampling time duration
           filename_locations='data\\selected_part_cologne_positions_'+str(step) # each csv-file for each step
           f = open('%s.csv'%filename_locations,'w',newline='')
           writer = csv.writer(f)
           for i in location_list:
               writer.writerow(i)
           f.close()
       
       vehicle_number = len(traci.vehicle.getIDList())
       print('step',step,"Total number of vehicles: " + str(vehicle_number))
       #calculate_distance(x_coordinate, y_coordinate, 0, 1)
       print()
       a += 1             
       step += 1
       index = 0
       x_coordinate = np.array([])
       y_coordinate = np.array([])
       
      
def main():    
    traci.start(sumoCmd)
    simpla.load("simpla_grid.xml")
    with open("selected_part_cologne_positions.txt", "w") as o:
        o.write("")
    vehicle_information()
    traci.close()

       
if __name__ == "__main__":
    main()