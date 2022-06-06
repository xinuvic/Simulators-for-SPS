# -*- coding: utf-8 -*-
"""
Created on Mon May  9 11:23:54 2022

@author: kevin
"""

import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
#add the "r" in front of the directory to avoid error message
sumoBinary = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "autobahn.sumocfg"]

import traci
import numpy as np
import math
import simpla



#calculate and output the euclidean distance between two cars
def calculate_distance(x_coordinate, y_coordinate, car1, car2):
    distance = round(math.sqrt(((abs(x_coordinate[car1]) - abs(x_coordinate[car2]))**2) + 
                         ((abs(y_coordinate[car1]) - abs(y_coordinate[car2]))**2)),2)
    print("Distance between car number " + str(car1) + " and car number " 
          + str(car2) + " is " + str(distance) + "m")
    
    

def vehicle_information():
    step = 0
    index = 0
   
    while step < 5000: 
       traci.simulationStep()
       x_coordinate = np.array([])
       y_coordinate = np.array([])       
       for vehicleId in traci.vehicle.getIDList():

           x, y = traci.vehicle.getPosition(vehicleId)           
           x_coordinate = np.append(x_coordinate, round(x,2))
           y_coordinate = np.append(y_coordinate, round(y,2))
                      
           #write the vehicle positions into the text file
           with open("autobahn_positions.txt", "a") as o:               
               o.write(str(step/10) + "," + vehicleId.replace(".", "") + "," 
                   + str(x_coordinate[index]) + "," + str(y_coordinate[index]) + "\n")              
           index +=1
    
       #calculate_distance(x_coordinate, y_coordinate,0,1) 
       total_vehicle_number = len(traci.vehicle.getIDList())
       print("Total number of vehicles is: " + str(total_vehicle_number))
       print()            
       step += 1
       index = 0
    
def main():    
    traci.start(sumoCmd)
    simpla.load("simpla.xml") #load the simpla file for platooning
    with open("autobahn_positions.txt", "w") as o: 
       o.write("")
    vehicle_information()
    traci.close()
       
if __name__ == "__main__":
    main()
    

