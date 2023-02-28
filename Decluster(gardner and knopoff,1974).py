'''
Programmed by: santosh kautwal
email- er.santoshkatuwal@gmail.com

Gardner and Knopoff, 1974
length= 10^(0.1238M+ 0.983)
Time=10^(0.032M+2.7389) if M>=6.5
Time=10^(0.5409M-0.547) if M<6.5

'''
import pandas as pd
import datetime as dt
import math
import os
from tqdm import tqdm
import time

cwd=os.getcwd()
data=pd.read_csv(cwd+'\homogenized.csv')
n=len(data)
data_copy=data      #copy of data for future use
date=[]
for i in range(0,n):
    date_i=dt.date(data.yyyy[i],data.mm[i],data.dd[i])
    date.append(date_i)
    
data=pd.DataFrame({'date':date,
                   'lat':data.latitude,
                   'lon':data.longitude,
                   'depth':data.depth,
                   'mag':data.mag,
                   'magType':data.magType})
data=data.sort_values(by='date',ascending=True)


for i in tqdm(range(0,n)):
    time.sleep(0)
    try:
        main=[]
        for j in range(i+1,n):
            try:
                tdiff=data.date[j]-data.date[i]
                T=tdiff.days
                
                #Calculating distance between two points
                '''
                Distance calculation between two coordinates using 'Spherical Law of Cosines'
                d = acos( sin φ1 ⋅ sin φ2 + cos φ1 ⋅ cos φ2 ⋅ cos Δλ ) ⋅ R
                φ1,φ2= latitudes of first and second coordinates
                Δλ=λ2-λ1 (longitude difference between two coordinates)
                if φ,λ in degrees,multiply φ,λ by (pi/180)to convert in radians
                R=4371000 m
                
                Example: distance between 1(lat1,long1) & 2(lat2,long2): 
                    1(27.671891,85.408580)& 2(27.939446,85.827244)
                
                '''
                x1=data.lat[i]*math.pi/180
                x2=data.lat[j]*math.pi/180
                
                y1=data.lon[i]* math.pi/180
                y2=data.lon[j]* math.pi/180
                
                L=math.acos(math.sin(x1)*math.sin(x2)+math.cos(x1)*math.cos(x2)*math.cos(y2-y1))*6371
                l=10**(0.1238*data.mag[j] + 0.983)
                if data.mag[j]>=6.5:
                    t=10**(0.032*data.mag[j]+2.7389)
                else:
                    t=10**(0.5409*data.mag[j]-0.547)
                    
                if L<=l and T<=t: #Aftershock Removal
                    if data.mag[i]>data.mag[j]:
                        
                        data=data.drop(index=j)
                    
                    else: #Foreshock Removal
                        data=data.drop(index=i)
                        i=j
                        break
            except:
                pass
    except:
        pass
data=data.reset_index()
data=data.drop(columns='index')

N=len(data)

yyyy=[]
mm=[]
dd=[]
for i in range(0, N):
    yyyy_i=data.date[i].year
    mm_i=data.date[i].month
    dd_i=data.date[i].day
    
    yyyy.append(yyyy_i)
    mm.append(mm_i)
    dd.append(dd_i)
    
datas=pd.DataFrame({'yyyy':yyyy,
                          'mm':mm,
                          'dd':dd,
                          'latitude':data.lat,
                          'longitude': data.lon,
                          'depth':data.depth,
                          'mag':data.mag,
                          'magType':data.magType})

datas.to_csv(cwd+'\\mainshock_only.csv', index = False)
    

    



    


