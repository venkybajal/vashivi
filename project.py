from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DATABASE_URL,Person,Interests
import json

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
    
	if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
		try:
			reqJson = json.loads(request.data)
		except:
			print "Response:"+request.data
			print "JSON body Error"
			return jsonify(status="failed",reason="JSON Body Error")
		if "phone" in reqJson and reqJson["phone"] != "" and len(reqJson["phone"]) == 10:
			phone =  reqJson["phone"]
			print "Phone:"+phone
		else:	
			print "Phone Number is Incorrect"
			return jsonify(status="failed",reason="Phone Number is Incorrect")

		if "name" in reqJson and reqJson["name"] != "":
			name =  reqJson["name"]
			print "Name:"+name
		else:	
			print "Name is Incorrect"
			return jsonify(status="failed",reason="Name is Incorrect")

		if "age" in reqJson and reqJson["age"] != "":
			age =  reqJson["age"]
			print "Age:"+age
		else:	
			print "AGE is Incorrect"
			return jsonify(status="failed",reason="Age is Incorrect")

		if "interests" in reqJson and reqJson["interests"] != "":
			interests =  reqJson["interests"]
			print "Interests:"+interests
		else:	
			print "Interests is Incorrect"
			return jsonify(status="failed",reason="Interests are Incorrect")

		if addInterest(interests,age,phone,name):
			session.commit();
			print "Successfully Added"
			return jsonify(status="success",reason="Added")
		else:
			print "Already Exists"
			return jsonify(status="failed",reason="Already Exists!")
	
	print "JSON Body or Header Incorrect!"		
	return jsonify(status="failed",reason="JSON Body or Header Incorrect!")

	'''
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
	'''
@app.route('/person/view/',methods=['POST'])
def viewPersonPost():
	if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
		try:
			reqJson = json.loads(request.data)
		except:
			return jsonify(status="failed",reason="JSON Body Error")
		if "phone" in reqJson and reqJson["phone"] != "" and len(reqJson["phone"]) == 10:
			phone =  reqJson["phone"]
			print "Phone Number: "+phone 
			person = session.query(Person).filter_by(phone = phone).first()
			interest = session.query(Interests).filter_by(phone = phone).all()
			if person:
				return jsonify(status = "success",data = person.serialize,interests=[r.serialize for r in interest])
			else:
				return jsonify(status = "success",reason="Not Found")
		return jsonify(status="failed",reason="Phone Number Incorrect")
	return jsonify(status="failed",reason="JSON Body or Header Incorrect!")



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

if __name__ == '__main__':
	app.debug = True
	app.secret_key = "kanilamba"
	app.run(host = '0.0.0.0', port = 5000)
