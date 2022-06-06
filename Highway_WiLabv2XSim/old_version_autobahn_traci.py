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
    
    
#add new vehicles on edge WE if current density is too low
def add_vehicles_WE(density_WE, a):              
    vehicle_number = traci.edge.getLastStepVehicleNumber("WE")
    print("Number of vehicles on edge WE: ", vehicle_number)
    edge_gone = density_WE - vehicle_number
    if edge_gone > 0:
        for i in range (edge_gone):
            traci.vehicle.add("WE_Lane_new" + str(a) + str(i), "r_0","car","now","random","base","10")

#add new vehicles on edge EW if current density is too low
def add_vehicles_EW(density_EW, a):              
    vehicle_number = traci.edge.getLastStepVehicleNumber("EW")
    print("Number of vehicles on edge EW: ", vehicle_number)
    edge_gone = density_EW - vehicle_number
    if edge_gone > 0:
        for i in range (edge_gone):
            traci.vehicle.add("EW_Lane_new" + str(a) + str(i), "r_1","car","now","random","base","10")
            

def vehicle_information():
    step = 0
    #density_WE = 60
    #density_EW = 60
    #a = 0
    index = 0
    x_coordinate = np.array([])
    y_coordinate = np.array([])
    
    while step < 5000: 
       traci.simulationStep()
       with open("autobahn_positions.txt", "a") as o:
           o.write("\n")           
           o.write("simulation step: " + str(step))
           o.write("\n")
       for vehicleId in traci.vehicle.getIDList():
           #list = traci.vehicle.getIDList();           
           #speed = traci.vehicle.getSpeed(vehicleId)
           x, y = traci.vehicle.getPosition(vehicleId)
           
           x_coordinate = np.append(x_coordinate, round(x,2))
           y_coordinate = np.append(y_coordinate, round(y,2))
           #write the vehicle positions into the text file
           with open("autobahn_positions.txt", "a") as o:               
               o.write("Vehicle ID : " + vehicleId + " x_coordinate: " + str(x_coordinate[index])
                     + "        y_coordinate: " + str(y_coordinate[index]))
               o.write("\n")                                     
           index +=1
                      
       #add_vehicles_WE(density_WE,a)
       #add_vehicles_EW(density_EW,a)
       
       #calculate_distance(x_coordinate, y_coordinate,0,1) 
       total_vehicle_number = len(traci.vehicle.getIDList())
       print("Total number of vehicles is: " + str(total_vehicle_number))
       print()
       #a += 1             
       step += 1
       index = 0
       x_coordinate = np.array([])
       y_coordinate = np.array([])

def main():    
    traci.start(sumoCmd)
    simpla.load("simpla.xml") #load the simpla file for platooning
    with open("autobahn_positions.txt", "w") as o: 
        o.write("")
    vehicle_information()
    traci.close()

       
if __name__ == "__main__":
    main()
    

