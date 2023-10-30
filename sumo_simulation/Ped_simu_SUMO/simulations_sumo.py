"""
Created on Wed Dec 29 01:47:07 2021
@author: XIN
"""

import numpy as np
import math 
import random
from random import choice
import pandas as pd
from ResSelectionInitial import ResSelectionInitial
from ConvertRowsintoColumns import ConvertRowsintoColumns
from CountConsecutiveColli import CountConsecutiveNumber
from Distance import Distance
from CalculateSINR import CalculateSINR
from RSSI import RSSI
from FindAccessibleRes import FindAccessibleRes
    
def SimulationwithSPS(ResSelectionini,TargetDistance,RClist,VehicleNum,StartTime,RCRange,StatisticVehicleRange):
    LowerBound=RCRange[0]
    HigherBound=RCRange[1]   
    AveRC=int(np.average(RCRange))
        
    RSSIEach = [0]*ResNum    
    RSSIEachStatistic=[[] for i in range(0,VehicleNum)]
    sumRSSI = []
    AverageRSSI = []
    PacketCollision = 0
    alltrans=0
    
    ReselectionTimeSpot=[]
    ResSelectionEachRound = [[] for i in range(0,VehicleNum)]
    ResSelectionall = [[] for i in range(0,VehicleNum)]

    ResSelectionEachRound = ResSelectionini[:]
    ResSelectionall = ResSelectionini[:]
    
    CollisionRecordAll=[[] for i in range(0,SimulationTime-StartTime)]
    ReselectionTimeSpot=[[] for i in StatisticVehicleRange]
    ReselectedRC=[[] for i in StatisticVehicleRange]
    for t in range(1,SimulationTime):
        
        # =============================================================================
        # for each timespot, import the location distribution
        # =============================================================================
        VehicleLocation = ObserveVehicles[t]
        if (t%50)==0:
            print('time:',t)
            
        # =============================================================================
        # SENSING AND SELECTION
        # =============================================================================
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
                        ReselectionTimeSpot[StatisticVehicleRange.index(i)].append(t)
                        ReselectedRC[StatisticVehicleRange.index(i)].append(RClist[i])
        ResSelectionall = ResSelectionEachRound[:]

        # =============================================================================
        # COLLISION RECORDING
        # =============================================================================
        if t in range(StartTime,SimulationTime):
            for i in StatisticVehicleRange:
                CollisionRecord = []
                for j in ConnectedVehiclesSetAll[i]:
                    if i == j:
                        continue
                    if Distance(i,j,VehicleLocation)<TargetDistance:
                        alltrans += 1
                        if CalculateSINR(i,j,ResSelectionall,VehicleNum,VehicleLocation,TransmitPower_mw)<sinr_th:
                            PacketCollision+=1
                            CollisionRecord.append(1)
                        else:
                            CollisionRecord.append(0)
                if CollisionRecord!=[]:
                    CollisionRecordAll[t-StartTime].append(CollisionRecord)
    return PacketCollision/alltrans,ReselectionTimeSpot,CollisionRecordAll,ReselectedRC


def run_simu(VehicleNum,TargetDistance,RCRange,ThresholdList):
    LowerBound=RCRange[0]
    HigherBound=RCRange[1]        
    RClist = [random.randint(LowerBound,HigherBound) for i in range(0,VehicleNum)] 
    
    PacketCollisionlist=[[]]*runningtime
    CollisionRecordlist=[[]]*runningtime
    AllCollisionRecord=[[]]*runningtime
    ReselectionTimeSpotlist=[[]]*runningtime
    ReselectedRClist=[[]]*runningtime
    StdPC=[]
      
    
    for s in range(0,runningtime):
        if (s%1==0):
            print('running time:',s)
        ResSelectionini= ResSelectionInitial(VehicleNum,ResNum)
        PacketCollision00,ReselectionTimeSpot,CollisionRecordAll,ReselectedRC = SimulationwithSPS(ResSelectionini,TargetDistance,RClist,VehicleNum,StartTime,RCRange,StatisticVehicleRange)        
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
            AllCollisionRecord[s]=ConvertRowsintoColumns(CollisionRecordlist[s])
            for i in range(0,len(StatisticVehicleRange)):
                SingleCollisionRecord = ConvertRowsintoColumns(AllCollisionRecord[s][i])
                success, fail, collision,count_selection = CountConsecutiveNumber(SingleCollisionRecord,1,ReselectionTimeSpotlist[s][i],SimulationTime,BeaconRate,ReselectedRClist[s][i],StartTime,maximalTime)
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
    print('\nvehicle number is', int(VehicleNum))
    ColRatio,colStd,del_ratio,delStd=run_simu(VehicleNum,TargetDistance,RCRange,ThresholdList)
    print('%s: Collision Probability'%str(RCRange),ColRatio,'std',colStd)
    print('%s: Delay Outage Probability'%str(RCRange),del_ratio,'std',delStd)


# =============================================================================
# Parameter setting
# =============================================================================
LaneNum=6
TargetDistance = 100
runningtime = 5
StartTime = 150
SimulationTime = 400
RCRange = [10,30]
BeaconRate = 20
print('beacon rate is',BeaconRate)
ResNum = int(2*(1000/BeaconRate))  
threshold=200
ThresholdList=[1000,500,200,100]
ProbabilityofPersistance = 0
print('Probability of Persistance:',ProbabilityofPersistance)

TransmitPowerdBm= 23
TransmitPower_mw = 10**(TransmitPowerdBm/10)
sinr_th_db = 2.76
sinr_th = 10**(sinr_th_db/10)

# =============================================================================
# import road traffic
# =============================================================================
ObserveVehicles = [[] for i in range(0,SimulationTime)]
LocationDataAll=np.array(pd.read_csv("sumo_vehicle_location.csv",header=None)).tolist()
VehicleNum=int(len(LocationDataAll)/SimulationTime)
for i in range(0,SimulationTime):
    ObserveVehicles[i]=LocationDataAll[int(i*VehicleNum):int((i+1)*VehicleNum)]  
#StatisticVehicleRange=range(int(VehicleNum*1/10),int(VehicleNum*9/10)+1)  


# =============================================================================
# vehicles for statistics
# =============================================================================
ConnectedVehiclesSetAll=[]
for i in range(0,int(VehicleNum)):
    ConnectedVehiclesSet = []
    
    for j in range(0,int(VehicleNum)):
        if i==j:
            continue
        count=0
        for t in range(StartTime,SimulationTime):
            if Distance(i, j, ObserveVehicles[t])<TargetDistance:
                count+=1
        if count==SimulationTime-StartTime:
            ConnectedVehiclesSet.append(j)
    ConnectedVehiclesSetAll.append(ConnectedVehiclesSet)    

StatisticVehicleRange=[]
for i in range(0,len(ConnectedVehiclesSetAll)):
    if ConnectedVehiclesSetAll[i]!=[]:
      StatisticVehicleRange.append(i)
                
        

# =============================================================================
# run the simulator
# =============================================================================
if __name__ == '__main__':
    main()

