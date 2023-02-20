import requests
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point

token = "6f298a6f68c27deb7dcd10aacef33abbd6819fdc"

WAQI_sensors = {
    "WackWack_Mandaluyong" : "https://api.waqi.info/feed/A132778/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Baltazar_Caloocan" : "https://api.waqi.info/feed/A64045/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Forbestown_Taguig" : "https://api.waqi.info/feed/A248974/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "SerendraBamboo_Taguig" : "https://api.waqi.info/feed/A50926/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Calzada_Taguig" : "https://api.waqi.info/feed/A204484/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc",
    "Multinational_Paranaque" : "https://api.waqi.info/feed/A127897/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
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

# to csv file
df = pd.DataFrame({'Sensor Name':Sensor_Name,'X':X_location,'Y':Y_location,'US AQI':US_AQI})
df.to_csv('IQAir_test.csv', index=False, encoding='utf-8')

# save to shapefile
geometry = [Point(xy) for xy in zip(df.X, df.Y)]
df = df.drop(['X', 'Y'], axis=1)
gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
gdf.to_file("./shapefiles/Philippines_Pollution.shp")