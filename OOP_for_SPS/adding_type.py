import numpy as np
import pandas as pd
from RBG import RBG
import time
from random import randrange
import csv

#print(randrange(10))
time_period_all=300000

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

for section_index in range(0,int(time_period_all/10000)):
    #location_file_name = 'sumo_vehicle_location_'+ str(section_index)
    location_file_name = 'manhattan_location_s20_'+ str(section_index)
    #location_file_name = 'sumo_vehicle_location' # + str(section_index)
    print('section_index',section_index)
    Data=np.array(pd.read_csv("C:/Users/adani/OneDrive/Documentos/GitHub/SimulatorSPS/OOP_for_SPS/traffic_data/%s.csv"%(location_file_name),header=None)).tolist()
    NewData=[]
    for i in range(0,len(Data)):
        p=randrange(10)
        type=[]
        #print(p) 
        if p>=0 and p<2:   
            type=1
        elif p>=2 and p<6:   
            type=2
        else:   
            type=3
        NewData.append([Data[i][0],Data[i][1],Data[i][2],type])
    
    filename='v2manhattan_location_s20_'+str(section_index)
    n=0
    f=open("C:/Users/adani/OneDrive/Documentos/GitHub/SimulatorSPS/OOP_for_SPS/traffic_data/%s.csv"%filename,'w',newline='')
    writer=csv.writer(f)
    for j in NewData:
        writer.writerow(j)
    f.close()
  