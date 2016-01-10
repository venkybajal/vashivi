from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem,Person

engine = create_engine('postgres://ytrvdxrnzzphvf:dfjwYJ8qoE859jy9MVvYsRSd9v@ec2-54-83-52-71.compute-1.amazonaws.com:5432/des6sj4shuk7v4')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id = 1):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
  return render_template('templates.html', restaurant=restaurant, items = items)
  
#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
  	newItem = MenuItem(name = request.form['name'],restaurant_id=restaurant_id)
  	session.add(newItem)
  	session.commit()
	flash("Item Created")
  	return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
  else:
  	return render_template('newitem.html',restaurant_id = restaurant_id)
  
#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
  if request.method == 'POST':
	if request.form['name']:
		editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Item edited")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
  else:
#USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
		return render_template('edititem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
  
#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(editedItem)
		session.commit()
		flash("Item Deleted")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
	#USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
		return render_template('deleteitem.html', restaurant_id = restaurant_id, item = editedItem)


@app.route('/person/add/<int:personid>/<string:name>')
def addPerson(personid,name): 
	newItem = Person(id = personid,name=name)
  	session.add(newItem)
  	session.commit()
	return jsonify(status="Added")


  
  

app.debug = True
app.secret_key = "kanilamba"
#app.run(host = '0.0.0.0', port = 5000)
