
# WeatherPy
The following is a Python script to help visualize the weather patterns of 500+ randomly selected cities across the world of varying distance from the equator. The data collected allows us to observe the following trends:
- The cities near the ecuator (with latitude = 0) show higher temperatures within a range of 60F to approx 100F. There is a strong negative correlation between the temperature and latitide. In other words, the more north a city is the lower the temperature reported. 
- The wind speed average around 8 to 10 mph across all sample cities. But otherwise show a weak correlation with respect to the latitude.
- The % cloudiness does not show to have any correlation with latitude. It averages around 40% but with a large variance of apprx 35. 
- The humidty % collected for this sample average is between 75% and 80%, with a large variance of 22 showing a weak correlation with latitude.


```python
# Dependencies
import requests as req
import time
from citipy import citipy
from random import randrange
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

    From 1500 random coordinates we generated a list of 633 different cities



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
        # show some progress and allow for time between server requests
        print('.',end='')
        time.sleep(1)
    except req.exceptions.RequestException as e:
        request_errors.append('str(e)')
        
print(f"Attempted {len(cities)} requests to Open Weather with random coordinates. {len(request_errors)} attempts failed")        

```

    Attempted 633 requests to Open Weather with random coordinates. 68 attempts failed



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
      <th>name</th>
      <th>temperature</th>
      <th>windspeed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>8</td>
      <td>100</td>
      <td>9.96</td>
      <td>Ranong</td>
      <td>81.4</td>
      <td>6.24</td>
    </tr>
    <tr>
      <th>1</th>
      <td>90</td>
      <td>79</td>
      <td>52.06</td>
      <td>Achim</td>
      <td>39.2</td>
      <td>13.87</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12</td>
      <td>100</td>
      <td>0.53</td>
      <td>Thinadhoo</td>
      <td>81.9</td>
      <td>1.32</td>
    </tr>
    <tr>
      <th>3</th>
      <td>75</td>
      <td>66</td>
      <td>-42.88</td>
      <td>Hobart</td>
      <td>53.6</td>
      <td>4.70</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>61</td>
      <td>60.17</td>
      <td>Helsinki</td>
      <td>15.8</td>
      <td>9.17</td>
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

    Avg = 73.94336283185841, Variance = 22.632282050181548



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

    Avg = 40.15221238938053, Variance = 34.93857095909948



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

    Avg = 8.733646017699101, Variance = 6.062160437109402



![png](figures/output_12_1.png)

