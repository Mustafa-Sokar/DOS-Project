from flask import Flask
from flask_restful import Api, Resource
from requests import request
import requests


app = Flask(__name__)
api = Api(app)

# we need to communicate with Catalog Server so we need Catalog IP Server
BASE0="http://"
BASE1 = "192.168.56.101:5000/"
# BASE2=input("Enter the IP Catalog server")

# making class 
class Purchase(Resource):
    # put takes bookNumber as argument
    def put(self,bookNumber):
        # We forward the request to the Catalog server to verify that the book is in stock by query then update.
        response=requests.put(BASE0+BASE1+"purchase/"+bookNumber)

        # return the order ID details after it's success purchased or failed if the book is out of stock
        return response.json()

# Add resourse 
api.add_resource(Purchase,"/purchase/<string:bookNumber>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)