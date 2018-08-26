class Order:
	def __init__(self, _id, restaurant_location, time):
		self.id = _id
		self.restaurant_location = restaurant_location
		self.time = time

class OrderAggregatorService:
	# A super simple ranking system - based on the time the order was placed
	# In a real system, take other flags (like say, priorityCustomer) into account	
	def orderRankingOnTime(self, orders):
		orders.sort(key=lambda x: x.time)
		return orders