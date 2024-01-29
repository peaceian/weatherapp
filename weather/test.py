import requests

url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization=CWB-869C7631-CE97-4263-9AF8-635DF71E8A67&locationId=F-D0047-003&elementName=WS"

class Records:
    def __init__(self):
        # self.locationName = locationName
        # ...
        pass

def main():
    res = requests.get(url)
    if res.status_code != 200:
        return

    data = res.json()
    # print(data)
    
    elementValue1 = []
    elementValue2 = []

    for i in data['records']['locations'][0]['location']:
        locationName = i['locationName']
        weatherElements = i['weatherElement'][0]['time'][0]['elementValue']
        for weatherElement in weatherElements:
            
            elementValue1.append(weatherElement)
            elementValue2.append(weatherElement)
            print(elementValue1)
            #print(elementValue1,elementValue2)
            #print(elementValue[0], elementValue[1])

if __name__ == "__main__":
    main()