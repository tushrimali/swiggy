import json
import requests
from Utilities import haversine_helper
from heapq import nsmallest

URL = "http://localhost:3000/DES/"

class DeliveryExecutiveService:	
	
	# Current this method pulls in all available DEs
	def gatherDeliveryExecutives(self):			
		executives = []
		r = requests.get(url = URL)
		data = r.json()
		
		for de in data:
			if de['state'] == 0:
				de_object = DeliveryExecutive(de['id'], de['currentLocation'], de['lastOrderDeliveredTime'])
				executives.append(de_object)

		return executives

	def sortBasedOnTimes(self, executives):
		return executives.sort(key=lambda x: x.lastOrderDeliveredTime, reverse=True)

	def sortBasedOnDistanceFromLocation(self, location):
		return executives.sort(key=lambda x: haversine_helper(location, x.location))

	def topNclosest(self, executives, location):
		closestNagents = (nsmallest(2, executives, key=lambda x: haversine_helper(location, x.location)))
		return closestNagents

	def highestWaitingTimeAgent(self, executives):
		executives.sort(key=lambda x: x.lastOrderDeliveredTime, reverse=True)
		return executives[0]

	def markExecutiveAsBusy(self, agent, orderId):
		r = requests.get(url = URL+str(agent.id))
		payload = r.json()
		payload['state'] = 1
		payload['currentOrder'] = orderId
		r = requests.put(url=URL+str(agent.id), data=json.dumps(payload), headers={'Content-Type': 'application/json'})



class DeliveryExecutive:
	def __init__(self, _id, location, lastOrderDeliveredTime):
		self.id = _id
		self.location = location
		self.lastOrderDeliveredTime = lastOrderDeliveredTime

