import json

class RestaurantService:	
	def gatherRestaurants(self):	
		restaurants_dump = [Restaurant("1", "lat1, long1"), Restaurant("2", "lat2, long2")]
		return restaurants_dump

class Restaurant:
	def __init__(self, id, location):
		self.id = id
		self.location = location