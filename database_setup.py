import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Restaurant(Base):
    __tablename__ = 'restaurant'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    menuItems = relationship("MenuItem",cascade = "all, delete-orphan")
 
class MenuItem(Base):
    __tablename__ = 'menu_item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) 


engine = create_engine('postgres://ytrvdxrnzzphvf:dfjwYJ8qoE859jy9MVvYsRSd9v@ec2-54-83-52-71.compute-1.amazonaws.com:5432/des6sj4shuk7v4')
 

Base.metadata.create_all(engine)
