import ast
from math import radians, cos, sin, asin, sqrt

def haversine_helper(restaurant_location, de_location):
	# convert decimal degrees to radians 
	(lat1, lon1) = ast.literal_eval(restaurant_location)
	(lat2, lon2) = ast.literal_eval(de_location)

	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	r = 6371 # Radius of earth in kilometers. Use 3956 for miles
	return c * r