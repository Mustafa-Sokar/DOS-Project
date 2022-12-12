from flask import Flask
from flask_restful import Api, Resource, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from requests import request
import requests

# creating the flask app
app = Flask(__name__)


#path for data base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

# creating an API object
api = Api(app)

# we need to communicate with front Server and the replica of the catalog server so we  IP's
BASE0="http://"
BASE1 = "192.168.1.103:5000/" # front server
BASE2 = "192.168.56.101:5001/" # catalog2 server


#initialize the database
db = SQLAlchemy(app)


# create Book Model for the DataBase 
class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    cost = db.Column(db.Integer,nullable=False)
    topic = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Book(title = {self.title},quantity = {self.quantity}, cost = {self.cost} ,topic = {self.topic})"

#create Database
with app.app_context():
    db.create_all()

# to make the output seralizable into Json we use fields
resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'quantity': fields.Integer,
    'cost': fields.Integer,
    'topic': fields.String
}

class Search (Resource):
    @marshal_with(resource_fields)
    def get(self, topicName):
        # filter by topicName, then ALL to return all items matching it
        result = BookModel.query.filter_by(topic=topicName).all()
        if not result:
            abort(404,message="sorry! could not find any Book related to that topic")
        return result
      
    
class Info(Resource):
    @marshal_with(resource_fields)
    def get(self, bookNumber):
        # filter by bookNumber(id) then return the first matching id
        result = BookModel.query.filter_by(id=bookNumber).first()
        if not result:
            abort(404,message="sorry! could not find any Book with that id")
        return result



 #first verify that the item with a specific id is in stock then decrement the number of items(books) in stock by one(update)
class Purchase(Resource):
    @marshal_with(resource_fields)

    def get(self, bookNumber):
        
        # filter by bookNumber(id)
        result = BookModel.query.filter_by(id=bookNumber).first()
        if not result:
           abort(404,message="sorry! could not find any Book with that id")
       
        if(result.quantity>0):
           return result
       


    def put(self, bookNumber):
        
        # filter by bookNumber(id)
        result = BookModel.query.filter_by(id=bookNumber).first()
        if not result:
            abort(404,message="sorry! could not find any Book with that id")        
        result.quantity=result.quantity-1
        if(result.quantity<0):
            abort(404,message="sorry! The Book is out of stock")
        db.session.commit()

        # for consistency for cache to clean old data and Consistency for replica
        requests.put("http://" + BASE2 + "purchase2/" + str(bookNumber))
        requests.put("http://" + BASE1 + "cache1/" + str(bookNumber))
        requests.put("http://" + BASE1 + "cache2/" + result.topic)


        abort(409,message="OK ,Book with id:"+str(bookNumber)+" Purchased Successfully")



class Purchase2(Resource):
    @marshal_with(resource_fields)

    def get(self, bookNumber):
        
        # filter by bookNumber(id)
        result = BookModel.query.filter_by(id=bookNumber).first()
        if not result:
           abort(404,message="sorry! could not find any Book with that id")
       
        if(result.quantity>0):
           return result
       


    def put(self, bookNumber):
        
        # filter by bookNumber(id)
        result = BookModel.query.filter_by(id=bookNumber).first()
        if not result:
            abort(404,message="sorry! could not find any Book with that id")        
        result.quantity=result.quantity-1
        if(result.quantity<0):
            abort(404,message="sorry! The Book is out of stock")
        db.session.commit()  
        #abort(409,message="OK ,Book with id:"+str(bookNumber)+" Purchased Successfully")

# adding the defined resources
api.add_resource(Search,"/search/<string:topicName>")
api.add_resource(Info,"/info/<int:bookNumber>")
api.add_resource(Purchase,"/purchase/<int:bookNumber>")
api.add_resource(Purchase2,"/purchase2/<int:bookNumber>")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)