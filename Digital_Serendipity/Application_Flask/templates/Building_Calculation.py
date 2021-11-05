import json,csv
import os
import ssl
import urllib.request
import sys
import pandas as pd


def Building_List_Appender(name, time, building_list):
    
    f = open('Final_Building_List.csv','a', newline='',encoding='utf-8-sig')
    wr = csv.writer(f)
    
    for i in range(0,len(building_list)):
        
        Final_Building_List =[name,time,building_list[i]]
        wr.writerow(Final_Building_List)

    print('List Save')
    
    return
