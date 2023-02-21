from routingpy import Valhalla
import json

client = Valhalla(base_url='http://localhost:8002')

coords = [[120.9927158,14.6096897],[121.0175177,14.6316460]]

with open("route_request_test2.json","r") as f:
    data = json.load(f)
    exclude_poly = data["features"][0]["geometry"]["coordinates"]

route = client.directions(locations=coords,instructions=True,profile="pedestrian",exclude_polygon=exclude_poly)

json_output = json.dumps(route.raw, indent=4)
with open("route_results.json","w") as f:
    f.write(json_output)

