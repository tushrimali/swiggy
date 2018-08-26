from DeliveryExecutiveService import DeliveryExecutiveService, DeliveryExecutive
from Order import Order, OrderAggregatorService

class AssignmentServer:
	def __init__(self):
		self.executiveService = DeliveryExecutiveService()
		self.orderAggregatorService = OrderAggregatorService()
	
	def start(self, input_orders):
		orders = []
		for order in input_orders:
			od = Order(order['id'], order['restaurant_location'], order['ordered_time'])
			orders.append(od)

		# Maintain some sort of ranking or scoring system to determine which order gets pushed to the top
		orders = self.orderAggregatorService.orderRankingOnTime(orders)
		return self.match(orders)

	# A super simple and unoptimized matching algorithm. Given a list of orders, it pulls in 2 closest DEs
	# And assigns a DE to each order based on the DEs waiting time
	def match(self, orders):
		output = []	

		for order in orders:
			
			# Ideally, you would poll the service till you get an available agent
			# I am going assume here that there is ALWAYS a valid agent available
			available_agents = self.executiveService.gatherDeliveryExecutives()
			
			# Fetch closest 2 agents
			closestNagents = self.executiveService.topNclosest(available_agents, order.restaurant_location)

			# Pick agent with the highest waiting time
			agent = self.executiveService.highestWaitingTimeAgent(closestNagents)

			# Assign (call any notfication services)
			assignment = {'de_id': agent.id, 'order_id': order.id}
			output.append(assignment)
			self.executiveService.markExecutiveAsBusy(agent, order.id)

		return output 