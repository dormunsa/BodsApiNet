import requests
import json
#weather Api properties
weatherApiKey = "4bdd7e1f295b41c7bf7e5014ebc046b3"


#get condition weather
def GetWeatherConditions(lat ,long):
    url = "https://api.weatherbit.io/v2.0/current"
    querystring = {"lat": lat, "lon": long, "key": weatherApiKey}
    response = requests.request("GET", url, params=querystring)
    json_data = json.loads(response.text)
    return json_data
#insert weather to db
def BuildWeatherObjectAndPot(weather , lat , long):
    city = (weather['data'][0]['city_name'])
    wind = weather['data'][0]['wind_spd']
    dsc = weather['data'][0]['weather']['description']
    data_set = {"LocationName": city,"Longitude": long,"Latitude":lat,"WindSpeed":wind,"Description":dsc }
    json_dump = json.dumps(data_set)
    response = requests.post('http://localhost:58157/api/Weather', json=data_set)
    json_data = json.loads(response.text)
    return json_data
