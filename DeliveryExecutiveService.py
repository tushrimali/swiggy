import json
import requests

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

