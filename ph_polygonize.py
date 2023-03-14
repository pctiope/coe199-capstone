import rasterio
import json
from rasterio.features import shapes

def polygonize(date_time):
    mask = None
    with rasterio.Env():
        with rasterio.open("./shapefiles/Philippines_Pollution_"+date_time+"_idw.tif") as src:
            image = src.read(1) # first band
            image = image.astype('int16')
            results = ({'type':'Feature','properties': {'AQI': v}, 'geometry': s} for s, v in shapes(image, mask=mask, transform=src.transform))
    geoms = list(results)
    output_dict = {"type": "FeatureCollection", "name": "polygonized", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": geoms}
    json_output = json.dumps(output_dict, indent=4)
    with open("./temp/polygonized_"+date_time+".json", "w") as outfile:
        outfile.write(json_output)