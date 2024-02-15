from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import json
from json import loads
import math
import urllib.request #讀取url
from urllib.request import urlopen
import re
import urllib.parse #解析url
from django.http import HttpResponse
import random
import urllib3
urllib3.disable_warnings()#Maybe appear InsecureRequestWarning, this could it disable.
import collections
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your views here.

user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
headers = {'user-agent': random.choice(user_agents)} #偽裝使用者

user_key = 'CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE'

def wr8(request):
    doc_name = 'F-C0032-001'
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/%s?Authorization=%s" % (doc_name,user_key)
    #headers = {'Connection':'close'}
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
    #headers = {'Connect':'close'}
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
    print(lat,lon,StationName,StationId,obsTime,Altitude,WDIR,WDSD,TEMP,HUMD,PRES,WEATHER,CITY,TOWN)


    all = zip(lat,lon,StationName,StationId,obsTime,Altitude,WDIR,WDSD,TEMP,HUMD,PRES,WEATHER,CITY,TOWN)
    return render(request,'realtimeweather.html',locals()) 
    

def detailone(request):
    if request.method == 'POST':
        detailone = request.POST['town']
        print(type(detailone))
        detailone = urllib.parse.quote(detailone)
        print(type(detailone))
        source1 = urllib.request.urlopen("https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?StationName="+detailone+"&Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE").read()
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
        city = urllib.parse.quote(city)#漢字轉譯成%xx%xx
        print(type(city))
        source = urllib.request.urlopen("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName="+city+"&Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE").read()
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

# def advisory(request):
    # url='https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0033-001?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE'
    # data = requests.get(url)
    # data_json = data.json()
    # locations = data_json['records']['location']

    # city = []
    # geocode = []
    # phenomena = []
    # significance = []
    # startime = []
    # endtime = []
    # hazards = []
    

    # for i in locations: 
        # city.append(i['locationName'])    # 縣市名稱
        # geocode.append(i['geocode'])    # 郵遞區號
        # if ['hazardConditions']['hazards']== True:
            # hazards=[]
            # phenomena.append(i['hazardConditions']['hazards'])
        # else:
            # phenomena.append(i['hazardConditions']['hazards'][0]['info'][1]['phenomena'])  # 現象
            # significance.append(i['hazardConditions']['hazards'][0]['info'][2]['significance'])  # 特報
            # startime.append(i['hazardConditions']['hazards']['validTime']['startTime'])    # 開始時間
            # endtime.append(i['hazardConditions']['hazards']['validTime']['endTime'])   # 降雨機率
            # print(f'城市：{city}，城市碼：{geocode}，{phenomena}{significance}')

            # phenomena.append(i['hazardConditions']['hazards'])
    
    # for i in locations: 
        # city.append(i['locationName'])    # 縣市名稱
        # geocode.append(i['geocode'])    # 郵遞區號
        # hazards.append(i['hazardConditions']['hazards'])
        # print(f'城市：{city}，城市碼：{geocode}，{hazards}')


    # all = zip(city,geocode,phenomena,significance,startime,endtime, hazards)
    # all2 = zip(city,geocode,hazards)
    # return render(request,'advisorieslist.html',locals())

def hello(request):
    return render(request,'homepage.html',locals())

def oneweek(request):
    if request.method == 'POST':
        locationName = request.POST['locationName']#.get is to get str
        #limit = request.POST['limit']
        #offset = request.POST['offset']
        #element = request.POST['element']
        #print(locationName,limit,offset,element)
        city = urllib.parse.quote(locationName)#漢字轉譯
        #url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE&limit=10&offset=10&locationName=%E5%AE%9C%E8%98%AD%E7%B8%A3&elementName=MaxAT'
        url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-089?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE&locationName='+city
        #url = urllib.request.urlopen('https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE&limit='+ limit +'&offset='+ offset + '&locationName=' + city + '&elementName=' + element).read()
        #url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE&limit={limit}&offset={offset}&locationName={city}&elementName={element}'
        #datalist = json.loads(url)  
        response = requests.get(url)
        datalist = response.json()
        #datalist = data_json['records']['locations']
        
        datasetDescription = []
        locationName = []
        geocode = []
        lat = []
        lon = []
        description = []
        startTime = []
        endTime = []
        elementInt = []
        measures = []
        
        
        
        for i in datalist:
            datasetDescription.append(i['records']['locations'][0]['datasetDescription'])
            locationName.append(i['records']['locations'][0]['location'][0]['locationName'])
            geocode.append(i['records']['locations'][0]['location'][0]['geocode'])
            lat.append(i['records']['locations'][0]['location'][0]['lat'])
            lon.append(i['records']['locations'][0]['location'][0]['lon'])
            description.append(i['records']['locations'][0]['location'][0]['weatherElement'][0]['description'])
            startTime.append(i['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][0]['startTime'])
            endTime.append(i['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][1]['endTime'])
            elementInt.append(i['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][2]['elementValue'][0]['value'])
            measures.append(i['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][2]['elementValue'][0]['measures'])
        print(f'datasetDescription:{datasetDescription}locationName:{locationName}geocode:{geocode}lat:{lat}lon:{lon}description:{description}startTime:{startTime}endTime:{endTime}elementInt:{elementInt}measure:{measures}')
        
        # for data in datalist:
            # datasetDescription.append(data['datasetDescription'])
            # locationName.append(data['location'][0]['locationName'])
            # geocode.append(data['location'][0]['geocode'])
            # lat.append(data['location'][0]['lat'])
            # lon.append(data['location'][0]['lon'])
            # description.append(data['location'][0]['weatherElement'][0]['description'])
            # startTime.append(data['location'][0]['weatherElement'][0]['time'][0]['startTime'])
            # endTime.append(data['location'][0]['weatherElement'][0]['time'][1]['endTime'])
            # elementInt.append(data['location'][0]['weatherElement'][0]['time'][2]['elementValue'][0]['value'])
            # measures.append(data['location'][0]['weatherElement'][0]['time'][2]['elementValue'][0]['measures'])
            # print(f'datasetDescription:{datasetDescription}locationName:{locationName}geocode:{geocode}lat:{lat}lon:{lon}description:{description}startTime:{startTime}endTime:{endTime}elementInt:{elementInt}measure:{measures}')
        all = zip(datasetDescription,locationName,geocode,lat,lon,description,startTime,endTime,elementInt,measures)
        #for data in datalist:
        #    data = {'datasetDescription':str(datalist['records']['locations'][0]['datasetDescription']),
        #     'locationName':str(datalist['records']['locations'][0]['location'][0]['locationName']),
        #         'geocode':str(datalist['records']['locations'][0]['location'][0]['geocode']),
        #         'lat':str(datalist['records']['locations'][0]['location'][0]['lat']),
        #         'lon':str(datalist['records']['locations'][0]['location'][0]['lon']),
        #         'description':str(datalist['records']['locations'][0]['location'][0]['weatherElement'][0]['description']),
        #         'startTime':str(datalist['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][0]['startTime']),
        #         'endTime':str(datalist['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][1]['endTime']),
        #         'elementInt':str(datalist['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][2]['elementValue'][0]['value']),
        #         'measures':str(datalist['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][2]['elementValue'][0]['measures']),
                 #'elementValue':str(datalist['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][2]['elementValue'][1]['value']),
                 #'measuressec':str(datalist['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][2]['elementValue'][1]['measures']),  
        # }
        #    print(data)
    else:
         data = {}
         print(data)

    return render(request,'oneweek.html',locals())

def cityweek(request):
    if request.method == 'POST':
        city = request.POST['city']#.get is to get str
        town = request.POST['town']
        elementName = request.POST['element']
        #print(type(elementName))
        town = urllib.parse.quote(town)
        print(town)
        #url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE&locationId=F-D0047-{city}&locationName={town}'
        url = urllib.request.urlopen('https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE&locationId=F-D0047-'+city+'&locationName='+town+'&elementName='+elementName).read()
        #url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE&locationId=F-D0047-'+city+'&locationName='+town
        #print(url)
        #request = requests.get(url)
        response = json.loads(url)
        #print(response)
        datacity = response['records']['locations']
        datalist = response['records']['locations'][0]['location']
        weather = response['records']['locations'][0]['location'][0]['weatherElement']
        time = response['records']['locations'][0]['location'][0]['weatherElement'][0]['time']
        element = response['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][0]['elementValue']
        Value1 = response['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][0]['elementValue'][0]['value']
        measures1 = response['records']['locations'][0]['location'][0]['weatherElement'][0]['time'][0]['elementValue'][0]['measures']
        #print(datalist)
        #print(type(datalist))
        #print(weather)    
        #print(elementpre)
        
        #create a dict method
        datalocations = []
        for data in datacity:
            datalocations.append({
                'datasetDescription':data['datasetDescription'],
                'locationsName':data['locationsName'],
                'dataid':data['dataid'],
            })
        print(datalocations)
        
        #create a list method 
        locationName = []
        geocode = []
        lat = []
        lon = []
        for data in datalist:
                locationName.append(data['locationName'])
                geocode.append(data['geocode'])
                lat.append(data['lat'])
                lon.append(data['lon'])
        print(locationName,geocode,lat,lon)
    #loop area
    #weatherelement 
        description = []
        for data in weather:
            description.append(data['description'])
        print(description)
    
    #time area for 1 week
        starttime = []
        endtime = []
        for data in time:
            starttime.append(data['startTime'])
            endtime.append(data['endTime'])
        print(starttime)
        print(endtime)
    
        
        #elementValue determine
        elementValue1 = []
        elementValue2 = []
        #impact!!
        for weatherElement in time:
            elementValue = weatherElement['elementValue']
            if len(elementValue) == 2:
                elementValue1.append(elementValue[0])
                elementValue2.append(elementValue[1])
            else:
                elementValue1.append(elementValue[0])
                
        print(type(elementValue1))    
        print(elementValue1,elementValue2)
        
    
    
        context = {'datalocations':str(datalocations),
                   'locationName':locationName,
                   'geocode':geocode,
                   'lat':lat,
                   'lon':lon,
                   'description':description,
                   'starttime':starttime,
                   'endtime':endtime,
                   'elementValue1':str(elementValue1),
                   'elementValue2':str(elementValue2),
                   #'elementValue':elementValue,
                   #'measuressec':measuressec,
               }
        all1 = zip(locationName,geocode,lat,lon,description)
        print(context)
    else:
        print('error')
        
    return render(request,'cityweek.html',locals())

