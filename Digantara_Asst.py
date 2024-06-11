#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install sgp4


# In[1]:


pip install pyproj


# In[1]:


from sgp4.api import accelerated
print(accelerated)


# In[ ]:


pip install --upgrade pyproj


# In[ ]:


import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import pyproj
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs72
from sgp4.ext import jday
import datetime
import os

def read_tle_data(file_path):

    satellites = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()
            satellite = twoline2rv(line1, line2, wgs72)
            satellites.append({'name': name, 'line1': line1, 'line2': line2, 'satellite': satellite})
    return satellites

def calculate_satellite_positions(satellites):
    def calculate_position(sat):
        satellite_obj = sat['satellite']
        positions = []
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(days=1)
        time_step = datetime.timedelta(minutes=1)

        current_time = start_time
        while current_time < end_time:
            year, month, day, hour, minute, second = current_time.timetuple()[:6]
            jd_ut_current = jday(year, month, day, hour, minute, second)
            position, velocity = satellite_obj.propagate(year, month, day, hour, minute, second)
            positions.append((current_time, position, velocity))
            current_time += time_step
        return positions

    num_cores = 4  # adjust the number of cores according to your machine
    positions = Parallel(n_jobs=num_cores)(delayed(calculate_position)(sat) for sat in satellites)
    return positions

def ecef2lla(pos):
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    transformer = pyproj.Transformer.from_proj(ecef, lla, always_xy=True)
    lon, lat, alt = transformer.transform(pos[0], pos[1], pos[2], radians=False)
    return lon, lat, alt

def convert_to_lla(positions):
    A = []
    for positions_sat in positions:
        for pos in positions_sat:
            time, ecef_pos, vel = pos
            lon, lat, alt = ecef2lla(ecef_pos)
            A.append((time, lat, lon, alt, vel[0], vel[1], vel[2]))
    return A

def filter_region(A, region):
    min_lat, max_lat, min_lon, max_lon = region
    filtered_data = [pos for pos in A if min_lat <= pos[1] <= max_lat and min_lon <= pos[2] <= max_lon]
    return filtered_data

def prompt_for_region():
    print("Enter the coordinates for the rectangular region:")
    print("Latitude 1, Longitude 1")
    lat1 = float(input("Latitude: "))
    lon1 = float(input("Longitude: "))

    print("Latitude 2, Longitude 2")
    lat2 = float(input("Latitude: "))
    lon2 = float(input("Longitude: "))

    print("Latitude 3, Longitude 3")
    lat3 = float(input("Latitude: "))
    lon3 = float(input("Longitude: "))

    print("Latitude 4, Longitude 4")
    lat4 = float(input("Latitude: "))
    lon4 = float(input("Longitude: "))

    min_lat = min(lat1, lat2, lat3, lat4)
    max_lat = max(lat1, lat2, lat3, lat4)
    min_lon = min(lon1, lon2, lon3, lon4)
    max_lon = max(lon1, lon2, lon3, lon4)

    return min_lat, max_lat, min_lon, max_lon

if __name__ == '__main__':
    file_name = '30sats.txt'
    file_path = os.path.join(os.getcwd(), file_name)
    satellites = read_tle_data(file_path)
    positions = calculate_satellite_positions(satellites)
    A = convert_to_lla(positions)
    region = prompt_for_region()
    filtered_data = filter_region(A, region)
    df = pd.DataFrame(filtered_data, columns=['Time', 'Latitude', 'Longitude', 'Altitude', 'Vx', 'Vy', 'Vz'])
    print(df.head())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




