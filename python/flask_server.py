# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 12:59:29 2019

@author: Drucare
"""

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
#from flask.ext.jsonpify import jsonify
from flask_jsonpify import jsonify

postgresConnString = "postgres://postgres:admin@192.168.2.55:5432/postgres"
sqliteConnString = "sqlite:///E:/files/python/chinook.db"
#sqliteConnString = "/root//chinook.db"
db_connect = create_engine(sqliteConnString)
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") 
		# This line performs query and returns json result
        #return {'employees': [ i[1] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
        #result = {'employees': [  query.cursor.fetchall()]}
        result = {'employees': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        print(result)
        return jsonify(result)
    
class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        #result = {'data': [ query.cursor.fetchall()]}
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
        

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')