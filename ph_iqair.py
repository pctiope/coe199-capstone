import requests
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from geopandas import GeoDataFrame
from shapely.geometry import Point
from time import time

IQAir_sensors = {
    "Multinational_Paranaque" : "https://www.iqair.com/philippines/ncr/paranaque/multinational-village",#waqi
    "Calzada_Taguig" : "https://www.iqair.com/philippines/ncr/taguig/calzada",#waqi
    "Forbestown_Taguig" : "https://www.iqair.com/philippines/ncr/taguig/forbestown-road",#waqi
    "NorthForbesPark_Makati" : "https://www.iqair.com/philippines/ncr/makati/north-forbes-park",
    "Dasmarinas_Makati" : "https://www.iqair.com/philippines/ncr/makati/dasmarinas-village",
    "AyalaCircuit_Makati" : "https://www.iqair.com/philippines/ncr/makati/circuit-ayala-outside",
    "WackWack_Mandaluyong" : "https://www.iqair.com/philippines/ncr/mandaluyong/wack-wack-greenhills",#waqi
    "Unioil_Shaw" : "https://www.iqair.com/philippines/ncr/mandaluyong/unioil-shaw",
    "Unioil_Blumentritt" : "https://www.iqair.com/philippines/ncr/san-juan/unioil-f-blumentritt",
    "Unioil_Cainta" : "https://www.iqair.com/philippines/calabarzon/rizal/unioil-cainta-ortigas-ext",
    "Unioil_Congressional" : "https://www.iqair.com/philippines/ncr/quezon-city/unioil-congressional-2",
    "Unioil_WestAve" : "https://www.iqair.com/philippines/ncr/quezon-city/unioil-west-ave",
    "Unioil_EdsaGuadalupe" : "https://www.iqair.com/philippines/ncr/makati/unioil-edsa-guadalupe-2",
    "Unioil_Meycauayan" : "https://www.iqair.com/philippines/central-luzon/meycauayan/unioil-meycauayan-bulacan"    # 0 always?
    # MISSING: Unioil Katipunan - Quezon Ave - Barangka - Conception, National Children's Hospital, Madison st. Greenhills
}

Sensor_Name = []
X_location = []
Y_location = []
US_AQI = []

start = time()
for sensor in IQAir_sensors:
    Sensor_Name.append(sensor)      # could automate sensor name using the html content
    X_location.append(0)            # temp values, still to add
    Y_location.append(0)            # temp values, still to add
    
    # page = urlopen(IQAir_sensors[sensor])
    # html = page.read().decode("utf-8")
    page = requests.get(IQAir_sensors[sensor])
    soup = BeautifulSoup(page.content, "html.parser")

    sensor_aqi = soup.find('p', attrs={'class':'aqi-value__value'}).string
    print(sensor_aqi)
    US_AQI.append(sensor_aqi)
print("Time Elapsed: "+str(time()-start)+" seconds")

# to csv file
df = pd.DataFrame({'Sensor Name':Sensor_Name,'X':X_location,'Y':Y_location,'US AQI':US_AQI})
df.to_csv('test_IQAir.csv', index=False, encoding='utf-8')

# save to shapefile
geometry = [Point(xy) for xy in zip(df.X, df.Y)]
df = df.drop(['X', 'Y'], axis=1)
gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
gdf.to_file("./shapefiles/Philippines_Pollution.shp")