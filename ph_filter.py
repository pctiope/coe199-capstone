import json
from shapely.geometry import Point, Polygon, shape, mapping
from shapely.ops import unary_union
import sys

threshold = 70
filename = "polygonized.json"
with open(filename) as f:
    data = json.load(f)
sorted_data = sorted(data['features'], key=lambda x: x["properties"]["AQI"], reverse=True)
temp = []
for polygon in sorted_data:
    if polygon["properties"]["AQI"] >= threshold and polygon["properties"]["AQI"] <= 500:   # if AQI > threshold
        coordinates = polygon["geometry"]
        temp.append(shape(coordinates))

if not len(temp): exit()                                                # stop if no polygons (temporary fix)
unions = unary_union(temp)
print(mapping(unions)["coordinates"])                                   # debugging
if (isinstance(mapping(unions)["coordinates"],list)):
    exclude_poly = [poly[0] for poly in mapping(unions)["coordinates"]]
elif (isinstance(mapping(unions)["coordinates"],tuple)):
    exclude_poly = mapping(unions)["coordinates"]
else:
    print("Something went wrong")
# print(exclude_poly)                                                   # debugging

output_dict = {"type": "FeatureCollection", "name": "filtered_output", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": [{"type": "Feature", "geometry": {"type": "Polygon","coordinates": exclude_poly}}]}
json_output = json.dumps(output_dict, indent=4)
with open("filtered.json", "w") as outfile:
    outfile.write(json_output)