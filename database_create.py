import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#Create instance of Class declarative base which can then be used to inherit the features of SQL Alchemy
Base = declarative_base()

#creates the Object Oriented table of restaurants which extends from the base class
class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    @property
    def serializeRest(self):
        #Returns object data in easily serializable format
        return {
            'name' : self.name,
            'id' : self.id,
        }

#creates the table of Menus
class MenuItem(Base):
    __tablename__ = 'menu'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        #Returns object data in easily serializable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
        }





#Creates the database and adds tables and columns
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.create_all(engine)
