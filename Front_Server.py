# using flask

from urllib import response
from flask import Flask
from flask_restful import Api, Resource
from requests import request
import requests

# creating the flask app
app = Flask(__name__)

# creating an API object
api = Api(app)

BASE0="http://"
# BASE1=input("Enter the IP Order server")
# BASE2=input("Enter the IP Catalog server")

BASE1 = "192.168.56.101:5000/" # catalog server
BASE2 = "192.168.56.102:5000/" # Order server


# making a class
class Search(Resource):
    def get(self,topicName):# corresponds to the get request for this resource
        #forward the search request to the Catalog server with topic name
        response = requests.get(BASE0+BASE1+"search/"+topicName)
        return response.json()
        


# making a class
class Info(Resource):
    def get(self,bookNumber):# corresponds to the get request for this resource
        #forward the Information request to the Catalog server with book number(id)
        response = requests.get(BASE0+BASE1+"info/"+bookNumber)
        return response.json()
        


# making a class
class Purchase(Resource):
    def put(self,bookNumber):# corresponds to the put request for this resource
        #forward the Purchase request to the Order server with book number(id)
        response = requests.put(BASE0+BASE2+"purchase/"+bookNumber)
        return response.json()


# adding the defined resources
api.add_resource(Search,"/search/<string:topicName>")
api.add_resource(Info,"/info/<string:bookNumber>")
api.add_resource(Purchase,"/purchase/<string:bookNumber>")

# driver function
if __name__ == "__main__":
    app.run(debug=True)
