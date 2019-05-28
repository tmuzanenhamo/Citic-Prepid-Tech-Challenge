import sqlite3 
from flask import Flask, request
from flask_restful import Resource

class User:
	def __init__(self, _id, username, password, firstname, lastname):
		self.id = _id
		self.username = username
		self.password = password
		self.firstname = firstname
		self.lastname = lastname

	
	# Creating mappings
	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('message_board.db') # Connecting to the database
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE username=?"
		result = cursor.execute(query, (username,))  

		row=result.fetchone()
		if row:
			user = cls(*row)   
		else:
			user = None

		connection.close()
		return user


	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('message_board.db') # Connect to the database
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE id=?"
		result = cursor.execute(query, (_id,))  

		row=result.fetchone()
		if row:
			user = cls(*row) 
		else:
			user = None

		connection.close()
		return user


class UserRegister(Resource): 
	def post(self):
		data = request.get_json()

		if User.find_by_username(data['username']):
			return {"message": "A user with that username already exists"}

		connection = sqlite3.connect('message_board.db')
		cursor = connection.cursor()

		query = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)"
		cursor.execute(query, (data['username'], data['password'], data['firstname'], data['lastname']))

		connection.commit()
		connection.close()

		return {"message": "Registration Sucessful"}, 201