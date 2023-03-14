from time import sleep
from datetime import datetime

from ph_aqi import init_sensors, get_sensor_data, df_to_csv, df_to_shp
from ph_idw import get_idw
from ph_polygonize import polygonize
from ph_filter import filter

while 1:
    format = "%d-%m-%Y_%H-%M-%S"        # dd-mm-yyyy_HH-MM-SS format
    date_time = datetime.now().strftime(format)

    #ph_aqi functions
    WAQI_sensors, IQAir_locations, IQAir_sensors = init_sensors()
    Sensor_Name, X_location, Y_location, US_AQI, df = get_sensor_data(WAQI_sensors, IQAir_locations, IQAir_sensors)
    df_to_csv(df, date_time)
    df_to_shp(df, date_time)

    #ph_idw functions
    get_idw(date_time)

    #ph_polygonize functions
    polygonize(date_time)

    #ph_filter functions
    threshold = 50
    filter(threshold, date_time)

    sleep(5)    # temporary, have to change to a more regular update interval