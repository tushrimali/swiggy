from DeliveryExecutiveService import DeliveryExecutiveService, DeliveryExecutive
from heapq import nsmallest
import ast
from math import radians, cos, sin, asin, sqrt

class AssignmentServer:
	
	def start(self, input_orders):
		orders = []
		for order in input_orders:
			od = Order(order['id'], order['restaurant_location'], order['ordered_time'])
			orders.append(od)

		# Maintain some sort of ranking or scoring system to determine which order gets pushed up to the top
		orders = self.orderRanking(orders)
		return self.match(orders)

	# A super simple and unoptimized matching algorithm. Given a list of orders, it pulls in available DEs
	# And assigns a DE to each order
	def match(self, orders):
		output = []	
		de_service = DeliveryExecutiveService()	# Your Delivery Executive Service being instantiated
		for order in orders:
			available_agents = de_service.gatherDeliveryExecutives()

			closest2agents = (nsmallest(2, available_agents, key=lambda x: self.haversine_helper(order.restaurant_location, x.location)))
			closest2agents.sort(key=lambda x: x.lastOrderDeliveredTime, reverse=True)

			agent = closest2agents[0]
			assignment = {'de_id': agent.id, 'order_id': order.id}
			output.append(assignment)
			de_service.markExecutiveAsBusy(agent, order.id)

		return output
			
	'''
	Calculate the great circle distance between two points  on the earth (specified in decimal degrees)
	'''
	def haversine_helper(self, restaurant_location, de_location):
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

	# A super simple ranking system - based on the time the order was placed
	# In a real system, take other flags (like say, priorityCustomer) into account
	def orderRanking(self, orders):
		orders.sort(key=lambda x: x.time, reverse=True)
		return orders


class Order:
	def __init__(self, _id, restaurant_location, time):
		self.id = _id
		self.restaurant_location = restaurant_location
		self.time = time