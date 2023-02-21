import requests
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point

from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import time

token = "6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
WAQI_sensors = {
    "WackWack_Mandaluyong" : "https://api.waqi.info/feed/A132778/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Baltazar_Caloocan" : "https://api.waqi.info/feed/A64045/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Forbestown_Taguig" : "https://api.waqi.info/feed/A248974/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "SerendraBamboo_Taguig" : "https://api.waqi.info/feed/A50926/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Calzada_Taguig" : "https://api.waqi.info/feed/A204484/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Multinational_Paranaque" : "https://api.waqi.info/feed/A127897/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
}

IQAir_sensors = {
    # "Multinational_Paranaque" : "https://www.iqair.com/philippines/ncr/paranaque/multinational-village", #waqi
    # "Calzada_Taguig" : "https://www.iqair.com/philippines/ncr/taguig/calzada", #waqi
    # "Forbestown_Taguig" : "https://www.iqair.com/philippines/ncr/taguig/forbestown-road", #waqi
    "NorthForbesPark_Makati" : "https://www.iqair.com/philippines/ncr/makati/north-forbes-park",
    "Dasmarinas_Makati" : "https://www.iqair.com/philippines/ncr/makati/dasmarinas-village",
    "AyalaCircuit_Makati" : "https://www.iqair.com/philippines/ncr/makati/circuit-ayala-outside",
    # "WackWack_Mandaluyong" : "https://www.iqair.com/philippines/ncr/mandaluyong/wack-wack-greenhills", #waqi
    "Unioil_Shaw" : "https://www.iqair.com/philippines/ncr/mandaluyong/unioil-shaw",
    "Unioil_Blumentritt" : "https://www.iqair.com/philippines/ncr/san-juan/unioil-f-blumentritt",
    "Unioil_Cainta" : "https://www.iqair.com/philippines/calabarzon/rizal/unioil-cainta-ortigas-ext",
    "Unioil_Congressional" : "https://www.iqair.com/philippines/ncr/quezon-city/unioil-congressional-2",
    "Unioil_WestAve" : "https://www.iqair.com/philippines/ncr/quezon-city/unioil-west-ave",
    "Unioil_EdsaGuadalupe" : "https://www.iqair.com/philippines/ncr/makati/unioil-edsa-guadalupe-2"
    # "Unioil_Meycauayan" : "https://www.iqair.com/philippines/central-luzon/meycauayan/unioil-meycauayan-bulacan"    # 0 always?
    # MISSING: Unioil Katipunan - Quezon Ave - Barangka - Conception, National Children's Hospital, Madison st. Greenhills
}

IQAir_locations = {
    # "Multinational_Paranaque" : [121.001488,14.486208], #waqi
    # "Calzada_Taguig" : [121.07563,14.536089], #waqi
    # "Forbestown_Taguig" : [121.043945,14.550762], #waqi
    "NorthForbesPark_Makati" : [121.035596,14.553975],
    "Dasmarinas_Makati" : [121.030732,14.56628],
    "AyalaCircuit_Makati" : [0,0],                          # TO GET
    # "WackWack_Mandaluyong" : [121.05573,14.591224], #waqi
    "Unioil_Shaw" : [0,0],                                  # TO GET
    "Unioil_Blumentritt" : [121.026652,14.6021],
    "Unioil_Cainta" : [121.125296,14.582285],
    "Unioil_Congressional" : [0,0],                         # TO GET
    "Unioil_WestAve" : [121.027586,14.644702],
    "Unioil_EdsaGuadalupe" : [121.025319,14.476359]
    # "Unioil_Meycauayan" : []    # 0 always?
    # MISSING: Unioil Katipunan - Quezon Ave - Barangka - Conception, National Children's Hospital, Madison st. Greenhills
}

Sensor_Name = []
X_location = []
Y_location = []
US_AQI = []
for sensor in WAQI_sensors:
    response = requests.request("GET", WAQI_sensors[sensor])
    Sensor_Name.append(sensor)
    X_location.append(response.json()["data"]["city"]["geo"][1])
    Y_location.append(response.json()["data"]["city"]["geo"][0])
    US_AQI.append(response.json()["data"]["aqi"])

start = time()
for sensor in IQAir_sensors:
    Sensor_Name.append(sensor)      # could automate sensor name using the html content
    X_location.append(IQAir_locations[sensor][0])
    Y_location.append(IQAir_locations[sensor][1])
    
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
df.to_csv('test_aqis.csv', index=False, encoding='utf-8')

# save to shapefile
geometry = [Point(xy) for xy in zip(df.X, df.Y)]
df = df.drop(['X', 'Y'], axis=1)
gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
gdf.to_file("./shapefiles/Philippines_Pollution.shp")