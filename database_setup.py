import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
DATABASE_URL = 'postgres://ytrvdxrnzzphvf:dfjwYJ8qoE859jy9MVvYsRSd9v@ec2-54-83-52-71.compute-1.amazonaws.com:5432/des6sj4shuk7v4'

class Person(Base):
    __tablename__ = 'person'


    name = Column(String(80), nullable = False)
    phone = Column(String(10), primary_key = True)
    interests = Column(String(500), nullable = False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.phone,
            'interests': self.interests
        }

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
