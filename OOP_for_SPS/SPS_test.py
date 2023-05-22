# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 00:19:25 2023

@author: CSUST
"""

from Vehicle import Vehicle
import numpy as np
import pandas as pd
from RBG import RBG
from Channel import Channel
import sys
import time
import argparse

parser = argparse.ArgumentParser(description=\
                                 '--r: running time,\
                                 \n--td: target distance for beacon message,\
                                 \n--sst: start sampling time,\
                                 \n--itv: transmission interval of beacon messages,\
                                 \n--rcl: RC lower bound,\
                                 \n--rch: RC higher bound,\
                                 \n--cr: fixed candidate ratio (0.1,0.2,0.3,0.4,0.5,0.6)')

                                
parser.add_argument('--cr', type=float, default=0.2)
parser.add_argument('--r', type=int, default=300000)
parser.add_argument('--td', type=float, default=200)
parser.add_argument('--sst', type=int, default=0)
parser.add_argument('--itv', type=int, default=100)
parser.add_argument('--rcl', type=int, default=5)
parser.add_argument('--rch', type=int, default=15)



def genearate_vehicles(num_vehicle, num_slot, vehicle_location, transmit_power, p_resource_keeping,RCrange,target_distance):
    vehicle_instance_list = []
    for i in range(num_vehicle):
        vehicle_instance_list.append(Vehicle(i,vehicle_location[i],transmit_power,p_resource_keeping,RCrange,target_distance))
    return vehicle_instance_list    
        
def generate_RBGs(num_slot,num_subch):
    RBG_intance_list = []
    for i in range(num_slot):
        RBG_intance_each_slot = []
        for j in range(num_subch):
            RBG_intance_each_slot.append(RBG(i,j))
        RBG_intance_list.append(RBG_intance_each_slot)
    return RBG_intance_list
  
 
def main(time_period,target_distance,start_sampling_time,interval,RC_low,RC_high,RSRP_ratio_beacon):
    # parameter settings
    transmit_power = 200
    time_period_all = 300000
    num_subch = 4
    
    RCrange = [RC_low,RC_high]
    #RSRP_ratio_beacon = 0.2
    p_resource_keeping = 0.4
    sensing_window = 1100
    
    sinr_th = 2**(2.1602)-1
    k0 = 10**(-4.38)
    alpha = 3.68
    
    num_RBs_per_RBG = 10
    SCS = 15*(10**3)
    num_sc_per_RB = 12
    bandwidth_per_RB = SCS * num_sc_per_RB
    bandwidth_per_RBG = bandwidth_per_RB * num_RBs_per_RBG
    noise_perhz_dBm = -174
    noise_perhz_mW = 10**(noise_perhz_dBm/10)
    noise = noise_perhz_mW * (bandwidth_per_RBG)

    pdr_ratio_list=[]
    transmission_condition=[]
    add_loss_ratio_to_beacon_list = []
    RSRP_th = -110
    candidate_ratio_list=[0.1,0.2,0.3,0.4,0.5]  

    filename='mh_fixcr_'+'_num_rep'+str(time_period)+'_interval'+str(interval)+\
        '_startpot'+str(start_sampling_time)+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    '''
    f = open('%s.log'%(filename), 'a')
    sys.stdout = f
    '''
    
    # =============================================================================
    # import road traffic
    # =============================================================================
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    for section_index in range(0,int(time_period_all/10000)):
        #location_file_name = 'sumo_vehicle_location_'+ str(section_index)
        location_file_name = 'manhattan_location_s20_'+ str(section_index)
        print('section_index',section_index)
        if section_index==0:
            LocationDataAll=np.array(pd.read_csv("traffic_data/%s.csv"%(location_file_name),header=None)).tolist()
        else:    
            LocationDataAll=np.vstack((LocationDataAll,np.array(pd.read_csv("traffic_data%s.csv"%(location_file_name),header=None)).tolist()))

    ObserveVehicles = [[] for i in range(0,time_period)]
    num_vehicle=int(len(LocationDataAll)/time_period_all)
    print('VehicleNum',num_vehicle)
    for i in range(0,time_period):
        ObserveVehicles[i]=LocationDataAll[int(i*num_vehicle):int((i+1)*num_vehicle)]  
    vehicle_location_ini = ObserveVehicles[0]



    print('time_period',time_period)
    print('start_sampling_time',start_sampling_time)
    print('RSRP_ratio_beacon',RSRP_ratio_beacon)
    print('p_resource_keeping',p_resource_keeping)
    print('sensing_window',sensing_window)
    print('num_vehicle',num_vehicle)
    print('num_subch', num_subch)
    print('interval', interval)
    print('transmit_power',transmit_power)
    print('target_distance',target_distance)
    
    # =============================================================================
    # initialization
    # =============================================================================
    vehicle_list = genearate_vehicles(num_vehicle,time_period,vehicle_location_ini,\
                                      transmit_power,p_resource_keeping,RCrange,target_distance)

    RBG_list = generate_RBGs(time_period,num_subch)
    channel = Channel(num_subch, interval)
    # generate messages
    for i in range(num_vehicle):
        vehicle_list[i].message_list_ini(time_period)
        vehicle_list[i].generate_beacon(interval, 200, time_period)
            
    # =============================================================================
    # run till time_period    
    # =============================================================================
    for t in range(0,time_period):
        if t%100==0: print('t=',t)
        for i in range(num_vehicle):
            # update location and sensing_window
            vehicle_list[i].update_location(ObserveVehicles[t][i])
            
            if t==0:
                # initialize resource selection
                vehicle_list[i].initial_RBGs_selection(RBG_list,interval) 
                vehicle_list[i].generate_neighbour_set(vehicle_list)
                
            else:
                vehicle_list[i].update_reselection_counter(t,interval,RCrange)
    
        # update sensing window, selection window and resource selection
        for i in range(num_vehicle):
            vehicle_list[i].generate_RBGlist_1100ms(t, RBG_list, sensing_window)
            vehicle_list[i].update_sensing_result(t, vehicle_list, RBG_list, sensing_window)
            
            if t>0:
                if vehicle_list[i].message_list[t]!=None:
                    vehicle_list[i].generate_neighbour_set(vehicle_list)
                    vehicle_list[i].generate_RBGs_in_selection_window(t,RBG_list,interval)
                    vehicle_list[i].RBG_selection_beacon(RSRP_ratio_beacon, RBG_list, t, channel)

            # statistic pdr for beacon messages
            if t>0 and t == vehicle_list[i].v_RBG.timeslot:
                vehicle_list[i].statistic_for_reception(vehicle_list,sinr_th,noise,t,start_sampling_time)
                    
        if t>start_sampling_time and t%1000==0:
            sum_tran = 0
            sum_rec = 0     
            sum_additional_loss_to_beacons = 0
            for vehicle in vehicle_list:
                vehicle.num_tran_em = 0
                vehicle.num_rec_em = 0
                sum_tran += vehicle.num_tran
                sum_rec += vehicle.num_rec
                vehicle.num_tran = 0
                vehicle.num_rec = 0
                
            add_loss_ratio_to_beacon_list.append(sum_additional_loss_to_beacons/(sum_additional_loss_to_beacons+sum_rec))
            pdr_ratio_list.append(sum_rec/sum_tran)
            transmission_condition.append([sum_rec,sum_tran])

            
    
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print('time_period',time_period)
    print('start_sampling_time',start_sampling_time)
    print('RSRP_ratio_beacon',RSRP_ratio_beacon)
    print('p_resource_keeping',p_resource_keeping)
    print('sensing_window',sensing_window)
    print('num_vehicle',num_vehicle)
    print('num_subch', num_subch)
    print('interval', interval)
    print('transmit_power',transmit_power)
    print('target_distance',target_distance)
    print('transmission_condition',transmission_condition)
    print('PDR:',pdr_ratio_list)
    print('Overall PDR:',list(map(sum, zip(*transmission_condition)))[0]/list(map(sum, zip(*transmission_condition)))[1])
    
    print('*******************')

    print('\n')         

    
if __name__ == '__main__':
    args = parser.parse_args()   # 解析所有的命令行传入变量
    main(args.r,args.td,args.sst,args.itv,args.rcl,args.rch,args.cr)



 
