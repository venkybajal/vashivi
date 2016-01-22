#author Venkat
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DATABASE_URL,Person,Interests,Friends
import json
import smtplib

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
	person = session.query(Person).all()
	interests = session.query(Interests).all()
	friends = session.query(Friends).all()
	return render_template('home.html',person = person, interests = interests,friends = friends )





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
				return jsonify(status = "success", data = person.serialize,interests=[r.serialize for r in interest])
			else:
				return jsonify(status = "success", reason="Not Found")
		return jsonify(status="failed", reason="Phone Number Incorrect")
	return jsonify(status="failed", reason="JSON Body or Header Incorrect!")

@app.route('/person/friend/add/',methods=['POST'])
def addFriendsPost():
	if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
		try:
			reqJson = json.loads(request.data)
		except:
			return jsonify(status="failed", reason="JSON Body Error")

		if "phone" in reqJson and reqJson["phone"] != "" and len(reqJson["phone"]) == 10:
			phone =  reqJson["phone"]
		else:
			return jsonify(status="failed",reason="Phone Number is Incorrect")

		if "email" in reqJson and reqJson["email"] != "":
			email =  reqJson["email"]
		else:
			return jsonify(status="failed",reason="Email is Incorrect")

		if "name" in reqJson and reqJson["name"] != "":
			name =  reqJson["name"]
		else:
			return jsonify(status="failed",reason="Name is Incorrect")

		if "user_phone" in reqJson and reqJson["user_phone"] != "" and len(reqJson["phone"]) == 10:
			user_phone =  reqJson["user_phone"]
		else:
			return jsonify(status="failed",reason="User Phone No is Incorrect")

		user = session.query(Person).filter_by(phone = user_phone).first()
		if user:
			newFriend = Friends(phone = phone, name=name, email = email, user_phone = user_phone)
			session.add(newFriend)
			session.commit()
			return jsonify(status="failed",reason="Friend Successfull Added")
		else:
			return jsonify(status="failed",reason="User Profile Doesn't Exist")


@app.route('/person/friend/view/',methods=['POST'])
def viewFriendsPost():

	if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
		try:
			reqJson = json.loads(request.data)
		except:
			return jsonify(status="failed", reason="JSON Body Error")

		if "phone" in reqJson and reqJson["phone"] != "" and len(reqJson["phone"]) == 10:
			phone =  reqJson["phone"]
		else:
			return jsonify(status="failed",reason="Phone Number is Incorrect")

		friend = session.query(Friends).filter_by(user_phone = phone).all()

		if friend:
			return jsonify(status="success", data=[r.serialize for r in friend])
		else:
			return jsonify(status="success", reason="Contact Not Available")
	return jsonify(status="success",reason="Header Error")

@app.route('/person/safemail/',methods=['POST'])
def send_mail_post():
	if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
		try:
			reqJson = json.loads(request.data)
		except:
			return jsonify(status="failed", reason="JSON Body Error")

		if "phone" in reqJson and reqJson["phone"] != "" and len(reqJson["phone"]) == 10:
			phone =  reqJson["phone"]
		else:
			return jsonify(status="failed",reason="Phone Number is Incorrect")

		friend = session.query(Friends).filter_by(user_phone = phone).all()
		person = session.query(Person).filter_by(phone = phone).first()
		email_list = get_all_mail(friend)
		print email_list
		for i in email_list:
			send_email(i,person.name)

		if friend:
			return jsonify(status="success")
		else:
			return jsonify(status="success", reason="Contact Not Available")
	return jsonify(status="success",reason="Header Error")


def get_all_mail(friend):
	lists = []
	for i in friend:
		lists.append(i.email)
	return lists

def get_message_content(name,recv):
	MESSAGE = 'Subject: %s\n\n%s' % ("Safe Alert",
	"""
	Hi,

	"""+name+""" is Safe.

	Thank You for your concern
	Sent By: Vashivi Social

	""")


 	return MESSAGE

def send_email(to_addr,name):
	# Credentials (if needed)
	username = 'venkybajal@gmail.com'
	password = open("passw.pass").read()

	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username, password)
	server.sendmail(username, to_addr, get_message_content(name))
	server.quit()

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
