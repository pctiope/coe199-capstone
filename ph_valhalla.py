import json
from subprocess import call

with open("route_request_test1.json","r") as f:
    data = json.load(f)
    x_start, y_start, x_end, y_end = data["start"][0], data["start"][1], data["end"][0], data["end"][1]

with open("filtered.json","r") as f:
    data = json.load(f)
    exclude_poly = data["features"][0]["geometry"]["coordinates"]

# input_data = {"locations":[{"lat":y_start,"lon":x_start},{"lat":y_end,"lon":x_end}],"costing":"pedestrian","exclude_polygons":exclude_poly}
# json_output = json.dumps(input_data)
# with open("input_data.json", "w") as outfile:
#    outfile.write(json_output)

input = str('{"locations":[{"lat":{},"lon":{}},{"lat":{},"lon":{}}],"costing":"pedestrian","exclude_polygons":{}}'.format(y_start,x_start,y_end,x_end,str(exclude_poly)))
call(["curl","http://localhost:8002/route","--data",input,">","output.json"])
