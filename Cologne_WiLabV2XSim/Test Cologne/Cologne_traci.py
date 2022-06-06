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
    

sumoBinary = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "selected_part_cologne.sumocfg"]

import traci
import numpy as np
import math
import simpla

def calculate_distance(x_coordinate, y_coordinate, car1, car2):
    distance = math.sqrt((x_coordinate[car1] - x_coordinate[car2])**2 + 
                         (y_coordinate[car1] - y_coordinate[car2])**2)
    print("distance between car number " + str(car1) + " and car number " 
          + str(car2) + " is " + str(distance) + "m")
    
    
def vehicle_information():
    step = 0
    index = 0
    
    while step < 5000:
       x_coordinate = np.array([])
       y_coordinate = np.array([])
       traci.simulationStep()
       for vehicleId in traci.vehicle.getIDList():
           x, y = traci.vehicle.getPosition(vehicleId)           
           x_coordinate = np.append(x_coordinate, round(x,2))
           y_coordinate = np.append(y_coordinate, round(y,2))
           
           #write the vehicle positions into the text file
           with open("selected_part_cologne_positions.txt", "a") as o:               
               o.write(str(step/10) + "," + vehicleId.replace(".", "") + "," 
                       + str(x_coordinate[index]) + "," + str(y_coordinate[index]) + "\n")                   
           index +=1       
       vehicle_number = len(traci.vehicle.getIDList())
       print("Total number of vehicles: " + str(vehicle_number))
       #calculate_distance(x_coordinate, y_coordinate, 0, 1)
       print()             
       step += 1
       index = 0
       
       
      
def main():    
    traci.start(sumoCmd)
    simpla.load("simpla_grid.xml")
    with open("selected_part_cologne_positions.txt", "w") as o:
        o.write("")
    vehicle_information()
    traci.close()

       
if __name__ == "__main__":
    main()