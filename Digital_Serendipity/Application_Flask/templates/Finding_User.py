import googlemaps
import folium
import time
import json,csv
import os
import ssl
import urllib.request
import sys
import pandas as pd
import folium
from math import sin, cos, sqrt, atan2, radians
import numpy as np

#Google API
gmaps_key = "AIzaSyDncpA_TIRwR0dqIaERSFlcIaVYuNIEx1U"
gmaps = googlemaps.Client(key=gmaps_key)

#Naver API
keyID = "nrmyamgrqp"
keyPW = "IhbMAZssfW9TAXzmOUJaA8QRb32aAxih2onYVrPL"

def New_User_Invitation():
            
    data = []
    row_index = 0
    with open("user_list.csv", "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        for row in reader:
            if row:  # avoid blank lines
                
                row_index += 1
                columns = [row[0],row[1], row[2],row[3]]
                data.append(columns)
    last_row = data[-1]
        
    return last_row

def Building_list_maker(Start_Building, End_Building):
    
    BuildingNo = pd.read_excel('Kaist_Building_No.xlsx')
    #building_location1
    building_location1 = gmaps.geocode("카이스트 "+Start_Building,language='ko')
    building_location2 = gmaps.geocode("카이스트 "+End_Building,language='ko')
    
    if building_location1[0]['geometry']['location'] == building_location2[0]['geometry']['location']:
        
        #startbuilding, endbuilding 찾기
        building1 = BuildingNo[BuildingNo['building'] == Start_Building]
        building2 = BuildingNo[BuildingNo['building'] == End_Building]

        #위도, 경도값 가져오기
        lat1 = building1['lat'].values[0]
        lng1 = building1['lon'].values[0]
        lat2 = building2['lat'].values[0]
        lng2 = building2['lon'].values[0]
        
    else:
        
        lat1 = building_location1[0]['geometry']['location']['lat']
        lng1 = building_location1[0]['geometry']['location']['lng']
        lat2 = building_location2[0]['geometry']['location']['lat']
        lng2 = building_location2[0]['geometry']['location']['lng']
    
    
    origin          = str(lng1)+","+str(lat1)
    destination     = str(lng2)+","+str(lat2)
    mode            = "walking"
    option          = "trafast"
    departure_time  = "now"

    url = "	https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start="+origin\
        +"&goal="+destination

    request         = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",keyID)
    request.add_header("X-NCP-APIGW-API-KEY",keyPW)
    context         = ssl._create_unverified_context()
    response        = urllib.request.urlopen(request, context=context)
    responseText    = response.read().decode('utf-8')
    responseJson    = json.loads(responseText)

    with open("./Agent_Transit_Directions.json","w") as rltStream :
        json.dump(responseJson,rltStream)

    wholeDict = None
    with open("./Agent_Transit_Directions.json","r") as transitJson :
        wholeDict = dict(json.load(transitJson))
        
    try:
        path = wholeDict["route"]
        stepList    = path["traoptimal"][0]["path"]
        
    except :        
        stepList = []

    #여기까지 StepList 저장

    #Buildng List 추출
    building_list = []
    R = 6373.0 

    for i in range(0,len(stepList)-1):
    
        distance = []
    
        for j in range(0,len(BuildingNo)-1):
            
            #거리계산
            lat_cmp = radians(BuildingNo.lat[j])
            lon_cmp = radians(BuildingNo.lon[j])
            lat_po = radians(stepList[i][1])
            lon_po = radians(stepList[i][0])    
            dlon = lon_cmp - lon_po
            dlat = lat_cmp - lat_po
    
            a = sin(dlat / 2)**2 + cos(lat_po) * cos(lat_cmp) * sin(dlon / 2)**2 
            c = 2 * atan2(sqrt(a), sqrt(1 - a))     
            distance_instance = R * c *1000    
            distance.append(distance_instance)

            #최소값 계산
            x = np.array(distance)
            min_distance = x.min()
        
            df = pd.DataFrame(distance)
            df['building'] = BuildingNo['building']
            df.columns = ['distance', 'building']
            
            #가장가까운 건물 계산
            for k in range(0,len(df)-1):
                if df.distance[k] ==min_distance:
                    #print("가장 가까운 건물은",df.building[k])
                    building_list.append(df.building[k])

    building_list = set(building_list)
    building_list = list(building_list)

    #건물 리스트 저장
    #f = open('user_building_list.csv','a', newline='',encoding='utf-8')
    #wr = csv.writer(f)
    #wr.writerow(building_list)
    print(building_list)

    
    return building_list

def Building_List_Comparison(building_list):
    
    Final_Building_List = pd.read_csv('Final_Building_List.csv')
    Intersection = pd.DataFrame(columns=['name','interbuilding','time'])
    
    inter_building = []
    building_user = []
    time_list = []

    #dataframe이랑 building 리스트 하나씩 비교
    for i in range(0,len(building_list)):
        for j in range(0,len(Final_Building_List.buildinglist)):
        
            if building_list[i] == Final_Building_List.buildinglist[j]:
                inter_building.append(building_list[i])
                good_user = Final_Building_List.name[j]
                same_time = Final_Building_List.time[j]
                time_list.append(same_time)
                building_user.append(good_user)
                
    result_user = building_user
    
    #Intersection 저장하기
    for i in range(0,len(inter_building)):
        
        Intersection = Intersection.append(pd.DataFrame([[building_user[i],inter_building[i],time_list[i]]],
                                                    columns = ['name','interbuilding','time']), ignore_index=True)
    result_user = list(set(building_user))
    result_time = list(set(time_list))
    print('building same user =',result_user)                         
    Intersection.to_excel('intersection.xlsx')
    
    return

def Time_Comparison(time):
    
    Intersection_List = pd.read_excel('intersection.xlsx')
    result_user = []
    
    
    #time 일치여부 확인
    for i in range(0,len(Intersection_List)):
        
        if time == Intersection_List.time[i]:
            time_user = Intersection_List.name[i]
            
            result_user.append(time_user)
            
    result_user = list(set(result_user))
    print("최종 일치하는 사용자는 ",result_user)
    
    return result_user


if __name__ == '__main__':

    #새로운 사용자 불러오기
    new_data = New_User_Invitation()
    name = new_data[0]
    start = new_data[1]
    end = new_data[2]
    time = new_data[3]

    #Building_list 계산
    building_list = Building_list_maker(start,end)

    #일치하는 building sorting
    Building_List_Comparison(building_list)

    #time 확인해서 최종 일치자 알려주기
    result_user = Time_Comparison(time)