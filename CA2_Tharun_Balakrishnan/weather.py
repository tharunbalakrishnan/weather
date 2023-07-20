import urllib.request
import json
import pymysql
from datetime import date, datetime, timedelta

BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/'

ApiKey='34ZUN597S8ZVGUJAUCBRNK57H'
UnitGroup='us'
Locations='Ireland'
QueryType='FORECAST'
AggregateHours='24'
StartDate = '2023-05-01'
EndDate='2023-07-18'

if QueryType == 'FORECAST':
    print(' - Fetching forecast data')
    QueryParams = 'forecast?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup + '&shortColumnNames=true'
    QueryParams = 'history?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup +'&startDateTime=' + StartDate + 'T00%3A00%3A00&endDateTime=' + EndDate + 'T00%3A00%3A00'

Locations='&locations='+Locations

ApiKey='&key='+ApiKey

URL = BaseURL + QueryParams + Locations + ApiKey+"&contentType=json"

print(' - Running query URL: ', URL)
print()


response = urllib.request.urlopen(URL)
data = response.read()
weatherData = json.loads(data.decode('utf-8'))

errorCode=weatherData["errorCode"] if 'errorCode' in weatherData else 0

if (errorCode>0):
    print("An error occurred retrieving the data:"+weatherData["message"])
    exit("Script terminated")
    
print( "Connecting to mysql database")

db = pymysql.connect(host="localhost", user="root",
                          passwd="naruto", port=3306)

cur = db.cursor()

insert_weather_data = ("INSERT INTO `weather_data_schema`.`weather_data`"
                "(`address`,`latitude`,`longitude`,`datetime`,`maxt`,`mint`,`temp`,`precip`,`wspd`,`wdir`,`wgust`,`pressure`)"
                "VALUES (%(address)s, %(latitude)s, %(longitude)s, %(datetime)s, %(maxt)s,%(mint)s, %(temp)s, %(precip)s, %(wspd)s, %(wdir)s, %(wgust)s, %(pressure)s)")

locations=weatherData["locations"]
for locationid in locations:  
    location=locations[locationid]
    for value in location["values"]:
        data_wx = {
        'address': location["address"],
        'latitude': location["latitude"],
        'longitude': location["longitude"],
        'datetime': datetime.utcfromtimestamp(value["datetime"]/1000.),
        'maxt':  value["maxt"] if 'maxt' in value else 0,
        'mint': value["mint"] if 'mint' in value else 0,
        'temp': value["temp"],
        'precip': value["precip"],
        'wspd': value["wspd"],
        'wdir': value["wdir"],
        'wgust': value["wgust"],
        'pressure': value["sealevelpressure"]
        }
        cur.execute(insert_weather_data, data_wx)
        db.commit()
               
cur.close() 
db.close()


