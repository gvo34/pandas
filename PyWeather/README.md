
# WeatherPy
The following is a Python script to help visualize the weather patterns of 500+ randomly selected cities across the world of varying distance from the equator. The data collected allows us to observe the following trends:
- The cities near the ecuator (with latitude = 0) show higher temperatures within a range of 60F to approx 100F. There is a strong negative correlation between the temperature and latitide. In other words, the more north a city is the lower the temperature reported. 
- The wind speed average around 8 to 10 mph across all sample cities. But otherwise show a weak correlation with respect to the latitude.
- The % cloudiness does not show to have any correlation with latitude. It averages around 40% but with a large variance of apprx 35. 
- The humidty % collected for this sample average is between 75% and 80%, with a large variance of 21 showing a weak correlation with latitude.


```python
# Dependencies
import requests as req
import time
from citipy import citipy
from random import randrange
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
#update config with api key 
from config import OpenWeather

```


```python
# create filenames for the output files
output_csv = "figures/WeatherPy.csv"
output_temp = "figures/WeatherPyTemperature.png"
output_cloud = "figures/WeatherPyCloudiness.png"
output_windsp = "figures/WeatherPyWindspeed.png"
output_humid ="figures/WeatherPyHumidity.png"
output_log = "log/WeatherPylogrequests.txt"
output_err = "log/WeatherPylogerrors.txt"
```


```python
# Input will be froom a selection of 500+ random coordinates. We want to generate a list a 500+ unique cities. 
num_coordinates = 1500
coordinates = [(randrange(-90,90), randrange(-180,180)) 
               for c in range(0,num_coordinates)]
cities = set()
for lat, lon in coordinates:
    cities.add(citipy.nearest_city(lat, lon).city_name)

print(f"From {len(coordinates)} random coordinates we generated a list of {len(cities)} different cities")
```

    From 1500 random coordinates we generated a list of 632 different cities



```python
# Setup endpoint information.
url = "http://api.openweathermap.org/data/2.5/weather"
```


```python
# Set query parameters
params = {'appid': OpenWeather,
          'q': '',
          'units': 'imperial'}
```


```python
# Loop through the list of cities and perform a request for data on each
weather_data = []
request_errors =[]
waiting = "|/-\\"
widx = 0

with open(output_log, 'w', newline='') as logfile:
    logfile.write("LOGFILE for City Weather Requests")
    for city in cities:
        # Get weather data
        params['q'] = city
        try:
            response = req.get(url, params=params)
            response.raise_for_status()
            weather_json = response.json()
            weather_data.append({'name':weather_json['name'],
                                 'temperature':weather_json["main"]["temp"],
                                'humidity':weather_json["main"]["humidity"],
                      'windspeed':weather_json["wind"]["speed"],
                      'cloudiness':weather_json["clouds"]["all"],
                      'latitude':weather_json["coord"]["lat"],
                      'longitude':weather_json['coord']['lon']})
            # log request
            logfile.write("\nCity: "+city +
                          "\nRequest: "+ str(response.url)+
                          "\nResponse " + str(response.status_code))
            
            # show some progress and allow for time between server requests
            print("Waiting "+ waiting[widx % len(waiting)] + "\r",end='')
            widx += 1
            time.sleep(.25)
        except req.exceptions.RequestException as e:
            request_errors.append("City: "+ city + " error " + str(e)+'\n')
            logfile.write("\nCity: "+city +
                          "\nRequest: "+ str(response.url)+
                          "\nResponse " + str(response.status_code) +
                         "\nError: "+str(e))
            
fails = len(request_errors)
total = len(cities)
success = total - fails
print("\r Completed")
print(f"{success} Successful requests from Open Weather. From a total of {len(cities)} attempts of random coordinates.")  
print(f"See request log in {output_log}")
print("--------------------------------")
if len(request_errors)>0:
    with open(output_err,'w', newline='\n') as errfile:
        print(f"See error log in {output_err}")
        errfile.write(f"{len(request_errors)} failed requests:\n")
        errfile.writelines(request_errors)
        #for err in request_errors:
        #    errfile.write(err)
```

     Completed
    558 Successful requests from Open Weather. From a total of 632 attempts of random coordinates.
    See request log in log/WeatherPylogrequests.txt
    --------------------------------
    See error log in log/WeatherPylogerrors.txt



```python
# Create Data Frame with weather data        
city_weather_df = pd.DataFrame(weather_data)
city_weather_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cloudiness</th>
      <th>humidity</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>name</th>
      <th>temperature</th>
      <th>windspeed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>75</td>
      <td>62</td>
      <td>37.46</td>
      <td>-122.43</td>
      <td>Half Moon Bay</td>
      <td>54.14</td>
      <td>11.41</td>
    </tr>
    <tr>
      <th>1</th>
      <td>92</td>
      <td>92</td>
      <td>37.02</td>
      <td>111.92</td>
      <td>Jiexiu</td>
      <td>31.64</td>
      <td>2.71</td>
    </tr>
    <tr>
      <th>2</th>
      <td>75</td>
      <td>69</td>
      <td>-17.53</td>
      <td>-149.33</td>
      <td>Tiarei</td>
      <td>80.60</td>
      <td>11.41</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>96</td>
      <td>16.32</td>
      <td>121.70</td>
      <td>Dumabato</td>
      <td>71.01</td>
      <td>3.71</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>68</td>
      <td>-37.88</td>
      <td>147.99</td>
      <td>Lakes Entrance</td>
      <td>74.34</td>
      <td>5.28</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Save data in a csv file
city_weather_df.to_csv(output_csv)
```


```python
# plot the relationship Temperature (F) vs. Latitude
fig = plt.figure(figsize=(10, 10))
ax=fig.add_subplot(111)
# Build a scatter plot for each data type
sns.regplot(x="latitude", y="temperature", data=city_weather_df)

# Incorporate the other graph properties
plt.title("Temperature in World Cities")
plt.ylabel("Temperature (Farenheit)")
plt.xlabel("Latitude")

# Save the figure
plt.savefig(output_temp)
plt.legend(loc='best')
plt.show()
```


![png](figures/output_9_0.png)



```python
# plot the relationship Humidity (%) vs. Latitude
fig = plt.figure(figsize=(10, 10))
ax=fig.add_subplot(111)

avg = city_weather_df['humidity'].mean()
variance = city_weather_df['humidity'].std()
print(f"Avg = {avg}, Variance = {variance}")
# Build a scatter plot for each data type
sns.regplot(x="latitude", y="humidity", data = city_weather_df)

# Incorporate the other graph properties
plt.title("Humidity in World Cities")
plt.ylabel("% Humidity")
plt.xlabel("Latitude")

# Save the figure
plt.savefig(output_humid)
plt.legend(loc='best')
plt.show()
```

    Avg = 76.1236559139785, Variance = 21.277278098266688



![png](figures/output_10_1.png)



```python
# plot the relationship Cloudiness (%) vs. Latitude
fig = plt.figure(figsize=(10, 10))
ax=fig.add_subplot(111)

avg = city_weather_df['cloudiness'].mean()
variance = city_weather_df['cloudiness'].std()
print(f"Avg = {avg}, Variance = {variance}")
# Build a scatter plot for each data type
sns.regplot(x="latitude", y="cloudiness", data = city_weather_df)

# Incorporate the other graph properties
plt.title("Cloudiness in World Cities")
plt.ylabel("% Cloudiness")
plt.xlabel("Latitude")

# Save the figure
plt.savefig(output_cloud)
plt.legend(loc='best')
plt.show()
```

    Avg = 39.74372759856631, Variance = 35.02316117592912



![png](figures/output_11_1.png)



```python
# plot the relationship Wind Speed (mph) vs. Latitude
fig = plt.figure(figsize=(10, 10))
ax=fig.add_subplot(111)

avg = city_weather_df['windspeed'].mean()
variance = city_weather_df['windspeed'].std()
print(f"Avg = {avg}, Variance = {variance}")
# Build a scatter plot for each data type
sns.regplot(x="latitude", y="windspeed", data = city_weather_df)

# Incorporate the other graph properties
plt.title("Wind Speed in World Cities")
plt.ylabel("Wind Speed (mph)")
plt.xlabel("Latitude")

# Save the figure
plt.savefig(output_windsp)
plt.legend(loc='best')
plt.show()
```

    Avg = 8.098458781362014, Variance = 5.699604520998323



![png](figures/output_12_1.png)

