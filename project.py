from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DATABASE_URL,Person,Interests

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
	person = session.query(Person).all()
	return render_template('home.html')



@app.route('/person/add/',methods=['POST'])
def addPersonPost():
	if "phone" in request.headers and request.headers["phone"] != "" and  len(request.headers["phone"])==10:
		phone = request.headers["phone"]
	else:
		return jsonify(status="failed",reason="Phone Number Incorrect")

	if "name" in request.headers and request.headers["name"] != "":
		name  = request.headers["name"]
	else:
		return jsonify(status="failed",reason="Name Incorrect")

	if "age" in request.headers:
		age  = request.headers["age"]
	else:
		return jsonify(status="failed",reason="Age Incorrect")
 
	if "interests" in request.headers and request.headers["interests"] != "":
		interests  = request.headers["interests"]
	else:
		return jsonify(status="failed",reason="Interests Incorrect")

	if addInterest(interests,age,phone,name):
		session.commit();

		return jsonify(status="success",reason="Added")
	else:
		return jsonify(status="failed",reason="Already Exists!")

@app.route('/person/view/',methods=['POST'])
def viewPersonPost():
	if "phone" in request.headers and request.headers["phone"] != "" and  len(request.headers["phone"])==10:
		phone = request.headers["phone"]
	else:
		return jsonify(status="failed",reason="Phone Number Incorrect")

	person = session.query(Person).filter_by(phone = phone).first()
	interest = session.query(Interests).filter_by(phone = phone).all()
	if person:
		return jsonify(status = "success",data = person.serialize,interests=[r.serialize for r in interest])
	else:
		return jsonify(status = "success",reason="Not Found")

def addInterest(interest,age,phone,name):
	interests_all = interest.split(",")
	session.begin(subtransactions=True)
	try:
		if not addPerson(age,phone,name):
			return False
		for i in interests_all:
		   newItem = Interests(phone = phone,name=i)
		   session.add(newItem)
		session.commit()
		session.commit()
		
		return True
		# transaction is not committed yet
	except:
		session.rollback() # rolls back the transaction, in this case
                   # the one that was initiated in method_a().
        raise

def addPerson(age,phone,name):
	session.begin(subtransactions=True)
	try:
		person = session.query(Person).filter_by(phone = phone).first()
		if person:
			return False
		newItem = Person(phone = phone,name=name,age = age)
		session.add(newItem)
		
		session.commit()
		return True

	except:
		session.rollback() # rolls back the transaction, in this case
                   # the one that was initiated in method_a().
        raise

app.debug = True
app.secret_key = "kanilamba"
#app.run(host = '0.0.0.0', port = 5000)
