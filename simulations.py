"""
Created on Wed Dec 29 01:47:07 2021
@author: XIN
"""

import numpy as np
import math 
import random
from random import choice
from GenerateVehicleLocation import GenerateVehicleLocation
from ResSelectionInitial import ResSelectionInitial
from ConvertRowsintoColumns import ConvertRowsintoColumns
from CountConsecutiveColli import CountConsecutiveNumber
from Distance import Distance
from CalculateSINR import CalculateSINR
from RSSI import RSSI
from FindAccessibleRes import FindAccessibleRes
    
def SimulationwithSPS(ResSelectionini,TargetDistance,RClist,VehicleNum,StartTime,VehicleLocation,RCRange,StatisticVehicleRange):
    LowerBound=RCRange[0]
    HigherBound=RCRange[1]   
    AveRC=int(np.average(RCRange))
        
    RSSIEach = [0]*ResNum    
    RSSIEachStatistic=[[] for i in range(0,VehicleNum)]
    sumRSSI = []
    AverageRSSI = []
    PacketCollision = 0
    alltrans=0
    CollisionRecordAll=[]
    ReselectionTimeSpot=[]
    ResSelectionEachRound = [[] for i in range(0,VehicleNum)]
    ResSelectionall = [[] for i in range(0,VehicleNum)]

    ResSelectionEachRound = ResSelectionini[:]
    ResSelectionall = ResSelectionini[:]
    
    CollisionRecordAll=[[] for i in StatisticVehicleRange]
    ReselectionTimeSpot=[[] for i in StatisticVehicleRange]
    ReselectedRC=[[] for i in StatisticVehicleRange]
    for t in range(1,SimulationTime):
        
        if (t%50)==0:
            print('time:',t)
        
        for i in range(0,VehicleNum):
            RClist[i]=RClist[i]-1
            RSSIEach = RSSI(i,ResSelectionall,ResNum,VehicleNum,VehicleLocation,TransmitPower_mw)
            RSSIEachStatistic[i].append(RSSIEach)
            if t<AveRC:
                sumRSSI = np.sum(RSSIEachStatistic[i],axis=0)
                AverageRSSI = [m/t for m in sumRSSI]
            else:
                sumRSSI = np.sum(RSSIEachStatistic[i][t-AveRC+1:],axis=0)
                AverageRSSI = [i/AveRC for i in sumRSSI]
            if RClist[i] == 0:
                RClist[i]=random.randint(LowerBound,HigherBound)
                p = random.random()
                if p > ProbabilityofPersistance:
                    temp = FindAccessibleRes(i,AverageRSSI,ResSelectionall,ResNum,0.2)
                    ResSelected = choice(temp)
                    ResSelection_i = ResSelected
                    ResSelectionEachRound[i] = ResSelection_i
                    if i in StatisticVehicleRange and t>=StartTime:
                        ReselectionTimeSpot[i-StatisticVehicleRange[0]].append(t)
                        ReselectedRC[i-StatisticVehicleRange[0]].append(RClist[i])
        ResSelectionall = ResSelectionEachRound[:]

        if t in range(StartTime,SimulationTime):
            s=0
            for i in StatisticVehicleRange:
                CollisionRecord = []
                for j in range(0,int(VehicleNum*4/4)):
                    if i == j:
                        continue
                    if Distance(i,j,VehicleLocation)<TargetDistance and CalculateSINR(i,j,ResSelectionall,VehicleNum,VehicleLocation,TransmitPower_mw)<sinr_th:
                        PacketCollision+=1
                        CollisionRecord.append(1)
                    elif Distance(i,j,VehicleLocation)<TargetDistance:
                        CollisionRecord.append(0)
                    if Distance(i,j,VehicleLocation)<TargetDistance:
                        alltrans += 1
                CollisionRecordAll[s].append(CollisionRecord)
                s+=1
    return PacketCollision/alltrans,ReselectionTimeSpot,CollisionRecordAll,ReselectedRC


def run_simu(VehicleNum,TargetDistance,RCRange,ThresholdList,IntraDistance):
    LowerBound=RCRange[0]
    HigherBound=RCRange[1]        
    RClist = [random.randint(LowerBound,HigherBound) for i in range(0,VehicleNum)] 
    
    PacketCollisionlist=[[]]*runningtime
    CollisionRecordlist=[[]]*runningtime
    AllCollisionRecord=[[]]*runningtime
    ReselectionTimeSpotlist=[[]]*runningtime
    ReselectedRClist=[[]]*runningtime
    StdPC=[]
    StatisticVehicleRange=range(int(VehicleNum*3/10),int(VehicleNum*7/10)+1)    
    
    for s in range(0,runningtime):
        if (s%1==0):
            print('running time:',s)
        VehicleLocation = GenerateVehicleLocation(VehicleNum,FirstVehicleLocation,VehicleLength,IntraDistance,LaneNum) 
        ResSelectionini= ResSelectionInitial(VehicleNum,ResNum)
        PacketCollision00,ReselectionTimeSpot,CollisionRecordAll,ReselectedRC = SimulationwithSPS(ResSelectionini,TargetDistance,RClist,VehicleNum,StartTime,VehicleLocation,RCRange,StatisticVehicleRange)        
        PacketCollisionlist[s]=PacketCollision00
        CollisionRecordlist[s]=CollisionRecordAll
        ReselectionTimeSpotlist[s]=ReselectionTimeSpot        
        ReselectedRClist[s]=ReselectedRC
    PacketCollision00 = sum(PacketCollisionlist)/float(len(PacketCollisionlist))
    PacketCollision00std = math.sqrt(sum([(i-PacketCollision00)**2 for i in PacketCollisionlist])/len(PacketCollisionlist))
    StdPC.append(PacketCollision00std)
    print('t from %d'%StartTime,'to %d'%int(SimulationTime))
    ACP=[]
    DOP=[]
    ACPStd=[]
    DOPStd=[]
    for threshold in ThresholdList:
        maximalTime=threshold/(1000/BeaconRate)
        ratiolist=[[]]*runningtime   
        ColRatiolist=[[]]*runningtime
        for s in range(0,runningtime):
            totalsuccess=0
            totalfail=0
            totalcollision=0
            total_count_selection=0
            for i in range(0,len(StatisticVehicleRange)):
                AllCollisionRecord[s]=ConvertRowsintoColumns(CollisionRecordlist[s][i])
                success, fail, collision,count_selection = CountConsecutiveNumber(AllCollisionRecord[s],1,ReselectionTimeSpotlist[s][i],SimulationTime,BeaconRate,ReselectedRClist[s][i],StartTime,maximalTime)
                totalsuccess += success
                totalfail += fail
                totalcollision += collision
                total_count_selection += count_selection
            ratiolist[s]=totalfail/(totalsuccess+totalfail)
            ColRatiolist[s]=totalcollision/total_count_selection
        OverallAverageRatio = np.average(ratiolist)
        overallCollisionRatio = np.average(ColRatiolist)
        ratiostd = math.sqrt(sum([(i-OverallAverageRatio)**2 for i in ratiolist]))/runningtime
        ColRatioStd = math.sqrt(sum([(i-overallCollisionRatio)**2 for i in ColRatiolist]))/runningtime
        ACP.append(overallCollisionRatio)
        DOP.append(OverallAverageRatio) # delay outage probability
        ACPStd.append(ratiostd)
        DOPStd.append(ColRatioStd)
    return ACP,ACPStd,DOP,DOPStd




def main():
    for VehicleDensityx4 in vehicle_all_in_simu:
        VehicleNum = VehicleDensityx4 # this is total number of all vehicles    
        VehicleDensity=VehicleDensityx4/4
        IntraDistance = 1000/(VehicleDensity/LaneNum)-4
        print('\nvehicle number is', int(VehicleDensity))
        ColRatio,colStd,del_ratio,delStd=run_simu(VehicleNum,TargetDistance,RCRange,ThresholdList,IntraDistance)
        print('%s: Collision Probability'%str(RCRange),ColRatio,'std',colStd)
        print('%s: Delay Outage Probability'%str(RCRange),del_ratio,'std',delStd)



# Parameter setting
LaneNum=6
vehicle_each_lane_withinkm=range(10,100,10)
vehicle_withinkm=[int(i*LaneNum) for i in vehicle_each_lane_withinkm]
vehicle_all_in_simu=[int(i*4) for i in vehicle_withinkm]
FirstVehicleLocation = [0,0]
TargetDistance = 100
runningtime = 1
StartTime = 150
SimulationTime = 250
RCRange = [10,30]
BeaconRate = 20
print('beacon rate is',BeaconRate)
ResNum = int(2*(1000/BeaconRate))  
threshold=200
ThresholdList=[1000,500,200,100]
ProbabilityofPersistance = 0
print('Probability of Persistance:',ProbabilityofPersistance)
VehicleLength = 4.0 
TransmitPowerdBm= 23
TransmitPower_mw = 10**(TransmitPowerdBm/10)
sinr_th_db = 2.76
sinr_th = 10**(sinr_th_db/10)

# run the simulator
if __name__ == '__main__':
    main()

