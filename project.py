from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DATABASE_URL,Person

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/person/add/<int:phone>/<string:name>/',methods=['GET','POST'])
def addPerson(phone,name): 
	if request.method == "GET":
		newItem = Person(id = phone,name=name)
  		session.add(newItem)
  		session.commit()
		return jsonify(Status="get added")

@app.route('/person/add/',methods=['POST'])
def addPersonPost():

	if request.headers["phone"] and request.headers["phone"] != "" and  len(request.headers["phone"])==10:
		phone = request.headers["phone"]
	else:
		return jsonify(status="failed",reason="Phone Number Incorrect")

	if request.headers["name"] and request.headers["name"] != "":
		name  = request.headers["name"]
	else:
		return jsonify(status="failed",reason="Name Incorrect")

	if request.headers["interests"] and request.headers["interests"] != "":
		interests  = request.headers["interests"]
	else:
		interests = ""

	person = session.query(Person).filter_by(id = phone).one()
	if person:
		return jsonify(status="failed",reason="Already Exists")

	newItem = Person(phone = phone,name=name,interests = interests)
	session.add(newItem)
	session.commit()
	return jsonify(status="success")

@app.route('/person/view/',methods=['POST'])
def viewPersonPost():
	if request.headers["phone"] and request.headers["phone"] != "" and  len(request.headers["phone"])!=10:
		phone = request.headers["phone"]
	else:
		return jsonify(status="failed",reason="Phone Number Incorrect")

	person = session.query(Person).filter_by(id = phone).one()
	if person:
		return jsonify(status = "success",data = person)
	else:
		return jsonify(status = "success",reason="Not Found")

if __name__ == '__main__':
	app.debug = True
	app.secret_key = "kanilamba"
	app.run(host = '0.0.0.0', port = 5000)
