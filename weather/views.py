from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import json
from json import loads
import math
import urllib.request
import re
import urllib.parse
from django.http import HttpResponse
import urllib3
urllib3.disable_warnings()#Maybe appear InsecureRequestWarning, this could it disable.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your views here.
user_key = 'CWB-869C7631-CE97-4263-9AF8-635DF71E8A67'

def wr8(request):
    doc_name = 'F-C0032-001'
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/%s?Authorization=%s" % (doc_name,user_key)
    headers = {'Connection':'close'}
    #requests setting remove SSL certificate.
    data = requests.get(url,headers=headers,verify=False) #requests json檔內容為文字
    print(data)
    #print(data.text)
    #data = requests.get(url).text #type:str

    data_json = data.json() #轉換json格式 #type:dict
    #data_json = json.loads(data) #json #type:dict

    
    
    locations = data_json['records']['location'] #取出location內容，依照API資料結構從最外層的鍵開始取出
    #locations = data_json



    city = []
    wr8 = []
    maxt8 = []
    mint8 = []
    ci8 = []
    pop8 = []
    starttime = []


    
    for i in locations: 
        city.append(i['locationName'])    # 縣市名稱
        wr8.append(i['weatherElement'][0]['time'][0]['parameter']['parameterName'])    # 天氣現象
        maxt8.append(i['weatherElement'][4]['time'][0]['parameter']['parameterName'])  # 最高溫
        mint8.append(i['weatherElement'][2]['time'][0]['parameter']['parameterName'])  # 最低溫
        ci8.append(i['weatherElement'][3]['time'][0]['parameter']['parameterName'])    # 舒適度
        pop8.append(i['weatherElement'][4]['time'][0]['parameter']['parameterName'])   # 降雨機率
        starttime.append(i['weatherElement'][0]['time'][0]['startTime']) #起始時間
        #print(f'{city}未來 8 小時{wr8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，體感{ci8}，降雨機率 {pop8}%，從{starttime}開始')
        #print(i)
        
    
    """
    for i in data_json: 
        city = i['locationName']  # 縣市名稱
        wr8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
        maxt8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']  # 最高溫
        mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
        ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']   # 舒適度
        pop8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 降雨機率
        print(f'{city}未來 8 小時{wr8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，體感{ci8}，降雨機率 {pop8} %')
        print(i)
        print(data_json)
    """
    all = zip(city,wr8,maxt8,mint8,ci8,pop8,starttime)


    

    return render(request,'weatherlist.html',locals())


def realtimeweather(request):
    doc_name = 'O-A0001-001'
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/%s?Authorization=%s" % (doc_name,user_key)
    headers = {'Connect':'close'}
    data = requests.get(url,headers=headers,verify=False)
    data_json = data.json()
    locations = data_json['records']['Station']


    lat = []
    lon = []
    StationName = []
    StationId = []
    obsTime = []
    Altitude = []
    WDIR = []
    WDSD = []
    TEMP = []
    HUMD = []
    PRES = []
    WEATHER = []
    CITY = []
    TOWN = []
    for i in locations:
        lat.append(i['GeoInfo']['Coordinates'][0]['StationLatitude'])
        lon.append(i['GeoInfo']['Coordinates'][0]['StationLongitude'])
        StationName.append(i['StationName'])
        StationId.append(i['StationId'])
        obsTime.append(i['ObsTime']['DateTime'])
        Altitude.append(i['GeoInfo']['StationAltitude'])
        WDIR.append(i['WeatherElement']['WindDirection'])
        WDSD.append(i['WeatherElement']['WindSpeed'])
        TEMP.append(i['WeatherElement']['AirTemperature'])
        HUMD.append(i['WeatherElement']['RelativeHumidity'])# round(float x [, n]  )
        PRES.append(i['WeatherElement']['AirPressure'])
        WEATHER.append(i['WeatherElement']['Weather'])
        CITY.append(i['GeoInfo']['CountyName'])
        TOWN.append(i['GeoInfo']['TownName'])


    all = zip(lat,lon,StationName,StationId,obsTime,Altitude,WDIR,WDSD,TEMP,HUMD,PRES,WEATHER,CITY,TOWN)
    return render(request,'realtimeweather.html',locals()) 
    

def detailone(request):
    if request.method == 'POST':
        detailone = request.POST['town']
        print(type(detailone))
        detailone = urllib.parse.quote(detailone)
        print(type(detailone))
        source1 = urllib.request.urlopen("https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?StationName="+detailone+"&Authorization=CWB-869C7631-CE97-4263-9AF8-635DF71E8A67").read()
        #print(source)
        #print(type(source))
        #listofdata = json.loads(source, strict=False)
        detaildata = json.loads(source1)
        #print(type(detaildata))

        data1 = {'StationName':str(detaildata['records']['Station'][0]['StationName']),
                'StationId':str(detaildata['records']['Station'][0]['StationId']),
                'obsTime':str(detaildata['records']['Station'][0]['ObsTime']['DateTime']),
                'lat':str(detaildata['records']['Station'][0]['GeoInfo']['Coordinates'][0]['StationLatitude']),
                'lon':str(detaildata['records']['Station'][0]['GeoInfo']['Coordinates'][0]['StationLongitude']),
                'Altitude':str(detaildata['records']['Station'][0]['GeoInfo']['StationAltitude']),
                'CITY':str(detaildata['records']['Station'][0]['GeoInfo']['CountyName']),
                'CoCode':str(detaildata['records']['Station'][0]['GeoInfo']['CountyCode']),
                'TOWN':str(detaildata['records']['Station'][0]['GeoInfo']['TownName']),
                'ToCode':str(detaildata['records']['Station'][0]['GeoInfo']['TownCode']),
                'WEATHER':str(detaildata['records']['Station'][0]['WeatherElement']['Weather']),
                'Precipitation':str(detaildata['records']['Station'][0]['WeatherElement']['Now']['Precipitation']),
                'WDIR':str(detaildata['records']['Station'][0]['WeatherElement']['WindDirection']),
                'WDSD':str(detaildata['records']['Station'][0]['WeatherElement']['WindSpeed']),
                'TEMP':str(detaildata['records']['Station'][0]['WeatherElement']['AirTemperature']),
                'HUMD':str(detaildata['records']['Station'][0]['WeatherElement']['RelativeHumidity']),
                'PRES':str(detaildata['records']['Station'][0]['WeatherElement']['AirPressure']),
                'PGS':str(detaildata['records']['Station'][0]['WeatherElement']['GustInfo']['PeakGustSpeed']),
                'HXWDIR':str(detaildata['records']['Station'][0]['WeatherElement']['GustInfo']['Occurred_at']['WindDirection']),
                'HXWDT':str(detaildata['records']['Station'][0]['WeatherElement']['GustInfo']['Occurred_at']['DateTime']),
                'DXTEMP':str(detaildata['records']['Station'][0]['WeatherElement']['DailyExtreme']['DailyHigh']['TemperatureInfo']['AirTemperature']),
                'DXTEMPT':str(detaildata['records']['Station'][0]['WeatherElement']['DailyExtreme']['DailyHigh']['TemperatureInfo']['Occurred_at']['DateTime']),
                'DNTEMP':str(detaildata['records']['Station'][0]['WeatherElement']['DailyExtreme']['DailyLow']['TemperatureInfo']['AirTemperature']),
                'DNTEMPT':str(detaildata['records']['Station'][0]['WeatherElement']['DailyExtreme']['DailyLow']['TemperatureInfo']['Occurred_at']['DateTime'])
                }
        print(data1)
    else:
        data1 = {}

    return render(request,'detailone.html',data1) 


def searchcity(request):
    if request.method == 'POST':
        city = request.POST['locationName']
        print(type(city))
        city = urllib.parse.quote(city)
        print(type(city))
        source = urllib.request.urlopen("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName="+city+"&Authorization=CWB-869C7631-CE97-4263-9AF8-635DF71E8A67").read()
        print(source)
        print(type(source))
        #listofdata = json.loads(source, strict=False)
        listofdata = json.loads(source)
        print(type(listofdata))
        #創立空字典裝入需要的鍵和值key:value
        data = {'locationName':str(listofdata['records']['location'][0]['locationName']),
            'wr8':str(listofdata['records']['location'][0]['weatherElement'][0]['time'][1]['parameter']['parameterName']),  #天氣現象
            'maxt8':str(listofdata['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']),  #最高溫
            'mint8':str(listofdata['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']),  #最低溫
            'ci8':str(listofdata['records']['location'][0]['weatherElement'][3]['time'][0]['parameter']['parameterName']),  #舒適度
            'pop8':str(listofdata['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']), #降雨機率
            'starttime':str(listofdata['records']['location'][0]['weatherElement'][0]['time'][0]['startTime'])#起始時間
            } 
        print(data)
    else:
        data = {}
        
        
        
        

    return render(request,'form.html',data) 

def advisory(request):
    url='https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0033-001?Authorization=CWB-869C7631-CE97-4263-9AF8-635DF71E8A67'
    data = requests.get(url)
    data_json = data.json()
    locations = data_json['records']['location']

    city = []
    geocode = []
    phenomena = []
    significance = []
    startime = []
    endtime = []
    hazards = []
    try:

        for i in locations: 
            city.append(i['locationName'])    # 縣市名稱
            geocode.append(i['geocode'])    # 郵遞區號
            phenomena.append(i['hazardConditions']['hazards'])
            phenomena.append(i['hazardConditions']['hazards']['info']['phenomena'])  # 現象
            significance.append(i['hazardConditions']['hazards']['info']['significance'])  # 特報
            startime.append(i['hazardConditions']['hazards']['validTime']['startTime'])    # 開始時間
            endtime.append(i['hazardConditions']['hazards']['validTime']['endTime'])   # 降雨機率
            print(f'城市：{city}，城市碼：{geocode}，{phenomena}{significance}')
    except:

        for i in locations: 
            city.append(i['locationName'])    # 縣市名稱
            geocode.append(i['geocode'])    # 郵遞區號
            hazards.append(i['hazardConditions']['hazards'])
            print(f'城市：{city}，城市碼：{geocode}，{hazards}')


    all = zip(city,geocode,phenomena,significance,startime,endtime)
    all2 = zip(city,geocode,hazards)
    return render(request,'advisorieslist.html',locals())
