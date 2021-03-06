# Swiggy Auto Assignment

## Python and Node modules required:

[json-server](https://www.npmjs.com/package/json-server): npm install -g json-server

[endpoints](https://pypi.org/project/endpoints/): pip install endpoints

## Steps to run the project
**1) json-server --watch db.json**

The above command instantiates and sets up a local server that houses your database. The database file here is db.json, and for the purposes of our project it will contain all our DE metadata. Try any of the following to get familiar with the server schema:
  
  All available agents: GET http://localhost:3000/DES
  
  Data for a Specific agent: GET http://localhost:3000/DES/{executive_id}

**2) endpoints --prefix=runServer --host=localhost:8000**

The above command gets our assignment service up and running at port 8000. Its a simple RESTful service that accepts orders from clients.

Subsequent requests to this endpoint would look like:
  
  POST http://localhost:8000/
  
  GET http://localhost:8000/

## Architecture ##

### runServer.py

Entry point for any request to the service. This is bolierplate code taken directly from the endpoints module documentation.

### DeliveryExecutiveService.py

A service that handles everything to do with Delivery Executives. It contains methods to communicate with your DE database (CRUD operations, fetching agents who are free, marking agents as busy etc.). Although beyond the scope of the assignment, this is the service where you would add additional additional interfaces to your DE database (say, maintain a cache of agents who are free, remove agents who've gone offline etc.)

### Order.py

Order: A class to contain order information

OrderAggregatorService: Rank orders coming thorugh. Ranking could be based on any of the following
- Order Placed Time
- Presence of Premium Customer Flag
- Orders in a high demand area

Appropriately, the 'queue' of the current batch of orders would also be more sophisticated (instead of a simple list like we have here)

### AssignmentServer.py

 The central piece of the assignment the AssignmentServer class. It contains the following methods:
 
**start**: Given a batch of input orders (when you hit the endpoint with an order list json), order them according to a scoring methodology (In this case, the scoring system being what order was placed the earliest)
 
**match**: Given a list of orders, process each order by fetching available DEs from our DB. Available agents are are ordered by their distance to the restaurant (first mile) and an agent with the highest waiting time is finally picked. 
Lastly, we send a HTTP PUT request to our DB server informing it that above agent needs to be taken off grid and is not available for further assignments in this batch.
 
My assignment system is extremely simple. Ideally I would like to assign a score (e.g. custom cost function) to each agent taking into account their closeness and waiting time (like say, 1.5 points for each km away from the restaurant and -1 point for every 5 minutes spend idle. The executive with the lowest score would then be assigned the order).

### Utilities.py

**haversine_helper**: Nothing fancy. A method to compute the distance between 2 points (taken from a post on stackoverflow)

### DB Schema

db.json contains the following fields:

- **id**: Delivery Executive's ID
- **currentLocation**: Delivery Executive's Current Location
- **state**: Delivery Executive's State (0 = Idle, 1 = TravelingToRestaurant, 2 = RestaurantToCustomer, 3 = Offline)
- **destinationLocation**: Customer Address
- **currentOrder**: Populated if an Order is being Delivered
- **pastOrders**: List of Past Orders (potential Keys into an Order Database)
- **lastOrderDeliveredTime**: Last Time the executive delivered an order

## Assumptions and Extensions

I've tried to emulate a real-time assignment system by adding an endpoint that processes a batch of Orders and queries/updates a DE database. In order for this to work correctly, an additional service/script/module would be required (a cron job equivalent) that regularly updates the DE's location in db.json (assuming a constant speed). If a DE has reached their destination location coordinates, we reset their state to Idle and add the order to the list of his/her past Orders.

- Assumption 1: Each DE gets mapped to a single order. This might not be the best scenario. In real life, a single DE can cater to multiple orders from a single restaurant.
- Assumption 2: Time in the input needs to be padded with a leading 0 if hour is a single digit. I haven't made the system particularly robust in terms of edge cases (input must be valid time, location should be valid coordinates etc.) and instead focused on ther overall modularity of the system
- Assumption 3: There must enough free agents at all times to pick an order


 
 
