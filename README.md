# Swiggy Auto Assignment Architecture

## Python and Node modules required:

npm install -g json-server

pip install endpoints

## Steps to run the project
**1) json-server --watch db.json**

The above command instantiates and sets up a local server that houses your database. The database file here is db.json, and for the purposes of our project it will contain all our DE metadata. Try any of the following:
  
  GET http://localhost:3000/DES
  
  GET http://localhost:3000/DES/1

**2) endpoints --prefix=runServer --host=localhost:8000**

The above command gets our assignment service up and running at port 8000. Its a simple RESTful service that accepts orders from clients.

Subsequent requests to this endpoint would look like:
  
  POST http://localhost:8000/
  
  GET http://localhost:8000/
