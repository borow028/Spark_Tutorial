#https://www.analyticsvidhya.com/blog/2015/08/data-scientist-meetup-hack/

apikey = '3146f5130697e385842246b291a2b25'
host = 'api.meetup.com'

#"https://api.meetup.com/2/groups?offset=0&format=json&topic=python&photo-host=public&page=20&radius=25.0&fields=&order=id&desc=false&sig_id=******&sig=*****************"
requesturl = 'https://api.meetup.com/2/groups?&sign=true&photo-host=public&topic=python&zip=55126&country=United States&city=minneapolis&state=mn&page=20'
signedurl = 'https://api.meetup.com/2/groups?zip=55126&offset=0&city=minneapolis&format=json&lon=-93.1299972534&topic=python&photo-host=public&state=mn&page=20&radius=25.0&fields=&lat=45.0900001526&order=id&desc=false&sig_id=209074588&sig=d40c19ca1435b2b5e297beb6b64cfc170b497d5e'

class MeetupHTTPErrorProcessor(HTTPErrorProcessor):
    def http_response(self, request, response):
        try:
            return HTTPErrorProcessor.http_response(self, request, response)
        except HTTPError, e:
            error_json = parse_json(e.read())
            if e.code == 401:
                raise UnauthorizedError(error_json)
            elif e.code in ( 400, 500 ):
                raise BadRequestError(error_json)
            else:
                raise ClientException(error_json)

import urllib
import json
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
#from meetup_api_client import *
import geopy as gp
import base64
import urllib2

geolocator = Nominatim()
places = [ "minneapolis","fargo"]# "california", "boston ", "new york" , "pennsylvania", "colorado", "seattle", "washington","los angeles", "san diego", "houston", "austin", "kansas", "delhi", "chennai", "bangalore", "mumbai" , "Sydney","Melbourne", "Perth", "Adelaide", "Brisbane", "Launceston", "Newcastle" , "beijing", "shanghai", "Suzhou", "Shenzhen","Guangzhou","Dongguan", "Taipei", "Chengdu", "Hong Kong"]
urls = [] #url lists
radius = 50.0 #add the radius in miles
data_format = "json"
topic = "Python" #add your choice of topic here
sig_id = "209074588" # initialize with your sign id, check sample signed key
sig = "d40c19ca1435b2b5e297beb6b64cfc170b497d5e" # initialize with your sign, check sample signed key

for place in places: 
 location = geolocator.geocode(place)
 urls.append("https://api.meetup.com/2/groups?offset=0&format=" + data_format + "&lon=" + str(location.longitude) + "&topic=" + topic + "&photo-host=public&page=500&radius=" + str(radius)+"&fields=&lat=" + str(location.latitude) + "&order=id&desc=false&sig_id=" +sig_id + "&sig=" + sig)
 
city,country,rating,name,members = [],[],[],[],[]
#-------------------------------------------------------------------------
#AUTHENTICATION ERROR
for url in urls:
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    data = data["results"] #accessed data of results key only

for url in urls:  
    headers = {'WWW-Authenticate': 'OAuth realm="%s"' % realm}
    data = ''    
    req = urllib2.Request(url, data, headers)    
    #response = urllib.urlopen(url)
    response = urllib2.urlopen(req).read() 
    data = json.loads(response.read())
    data= data["results"] #accessed data of results key only
#-------------------------------------------------------------------------   
 
for i in data :
 city.append(i['city'])
 country.append(i['country'])
 rating.append(i['rating'])
 name.append(i['name'])
 members.append(i['members']) 
 
df = pd.DataFrame([city,country,rating,name,members]).T
df.columns=['city','country','rating','name','members']

df.head()

#Number of Python groups across six countries
freq = df.groupby('country').city.count() 
fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(121)
ax1.set_xlabel('Country')
ax1.set_ylabel('Count of Groups')
ax1.set_title("Number of Python Meetup Groups")
freq.plot(kind='bar') 

#Average size of groups across countries
freq = df.groupby('country').members.sum()/df.groupby('country').members.count()
fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(121)
ax1.set_xlabel('Country')
ax1.set_ylabel('Average Members in each group')
ax1.set_title("Python Meetup Groups")
freq.plot(kind='bar')

#Average rating of groups across countries
freq = df.groupby('country').rating.sum()/df.groupby('country').rating.count()
fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(121)
ax1.set_xlabel('Country')
ax1.set_ylabel('Average rating')
ax1.set_title("Python Meetup Groups")
freq.plot(kind='bar')

#Top 2 groups for each country
df=df.sort(['country','members'], ascending=[False,False])
df.groupby('country').head(2)




 