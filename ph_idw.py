from pyidw import idw

idw.idw_interpolation(
    input_point_shapefile="./shapefiles/Philippines_Pollution.shp",
    extent_shapefile="./shapefiles/Philippines_Border.shp",
    column_name="US AQI",
    power=2,
    search_radious=15,
    output_resolution=250,
)