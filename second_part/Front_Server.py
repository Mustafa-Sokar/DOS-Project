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

BASE3 = "192.168.56.101:5001/" #catalog2 server
BASE4 = "192.168.56.102:5001/" # Order2 server

flag_Catalog = 0
flag_Order = 0
cache = {}


# making a class
class Search(Resource):
    def get(self,topicName):# corresponds to the get request for this resource

        global flag_Catalog
        global cache

        #first we check if the request is in cache
        if topicName in cache:
            return cache[topicName]

        else:#forward the search request to the Catalog server with load balancing
            if flag_Catalog==0:
                response = requests.get(BASE0+BASE1+"search/"+topicName)
                # we store the data in cache
                cache[topicName]=response.text
                flag_Catalog=1

            else:
                response = requests.get(BASE0+BASE3+"search/"+topicName)
                # we store the data in cache
                cache[topicName]=response.text
                flag_Catalog=0

            return response.json()
        


# making a class
class Info(Resource):
    def get(self,bookNumber):# corresponds to the get request for this resource

        global flag_Catalog
        global cache

        #first we check if the request is in cache
        if bookNumber in cache:
            return cache[bookNumber]

        else:#forward the Information request to the Catalog server with load balancing
            if flag_Catalog==0:
                response = requests.get(BASE0+BASE1+"info/"+bookNumber)
                # we store the data in cache
                cache[bookNumber]=response.text
                flag_Catalog=1

            else:
                response = requests.get(BASE0+BASE3+"info/"+bookNumber)
                # we store the data in cache
                cache[bookNumber]=response.text
                flag_Catalog=0

            return response.json()
        
        


# making a class
class Purchase(Resource):
    def put(self,bookNumber):# corresponds to the put request for this resource

        global flag_Order

        #forward the Purchase request to the Order server with load balancing
        if flag_Order==0:
            response = requests.put(BASE0+BASE2+"purchase/"+bookNumber)
            flag_Order=1
        else:
            response = requests.put(BASE0+BASE4+"purchase/"+bookNumber)
            flag_Order=0

        return response.json()


#the data for the Book with id removed from the cache
class cache1(Resource):

    def put(self, bookNumber):
        del cache[bookNumber]

#the data for the Book with topicName removed from the cache
class cache2(Resource):

    def put(self, topicName):
        del cache[topicName]

# adding the defined resources
api.add_resource(Search,"/search/<string:topicName>")
api.add_resource(Info,"/info/<string:bookNumber>")
api.add_resource(Purchase,"/purchase/<string:bookNumber>")
api.add_resource(cache1, "/cache1/<string:bookNumber>")
api.add_resource(cache2, "/cache2/<string:topicName>")


# driver function
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
