import os
from flask import Flask ,flash,jsonify,request
import json
app = Flask(__name__)

class RoutePoint():
	def __init__(self,dn):
		self.dn = dn
		self.counter1 = 0
		self.counter2 = 0
		self.interest = ""

	def get_number(self):
		return self.dn

	def  set_interest(self, interest):
		self.interest = interest

	def get_interest(self):
		return self.interest

	def increment_counter_1(self):
		self.counter1 += 1

	def get_increment_counter_1(self):
		return self.counter1

	def increment_counter_2(self):
		self.counter2 += 1

	def get_increment_counter_2(self):
		return self.counter2



dn_9501 =  RoutePoint('9501')
dn_9502 =  RoutePoint('9502')
dn_9503 =  RoutePoint('9503')
dn_9504 =  RoutePoint('9504')
dn_9505 =  RoutePoint('9505')

list_dn = [dn_9501,dn_9502,dn_9503,dn_9504,dn_9505]


def process_dn(interest):
	for i in list_dn: 
		if i.get_interest().upper() == interest.upper() and i.get_increment_counter_1() < 2:
			i.increment_counter_1()
			return i
	
	for i in list_dn:
		if i.get_increment_counter_1() == 0:
			i.increment_counter_1()
			return i




		
def get_dn(number):
	for i in list_dn:
		if i.get_number() == number:
			return i
	return None


@app.route('/stranger/get_dn/',methods=['POST'])
def get_dn_stranger():
	if "Content-Type" in request.headers and request.headers["Content-Type"] == "application/json":
		try:
			request_json = json.loads(request.data)
		except:
			return jsonify(status="failed", reason="JSON Body Error")

		if request_json["feature"] == "1":
			print "Feature: "+request_json["feature"]
			interest = request_json["interest"]
			print "Interest: "+interest
			i = process_dn(interest)
			print "DN Selected: "+i.get_number()
			if i:
				i.set_interest(interest)
				return jsonify(status = "success", dn=i.get_number())
			else:
				return jsonify(status = "failed", reason="No DN available")

		elif request_json["feature"] == "2":
			print "Feature: "+request_json["feature"]
			dn = request_json["dn"]
			print "DN reqested: "+str(dn)
			i = get_dn(str(dn))
			if i:
				print "DN Selected: "+i.get_number()
				i.increment_counter_2()
				return jsonify(status = "success",count = i.get_increment_counter_2())
			else:
				return jsonify(status = "failed", reason="No DN available")

	return jsonify(status = "failed",reason="Content-type not specified")


if __name__ == '__main__':
	app.debug = True
	app.secret_key = "kanilamba"
	app.run(host = '0.0.0.0', port = 5000)
