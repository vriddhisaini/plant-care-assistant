from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plant(Base):
    __tablename__ = 'plants'
    plant_id = Column(String(100), primary_key=True)
    scientific_name = Column(String(100))
    difficulty = Column(String(50))

    names = relationship('PlantName', back_populates='plant', cascade="all, delete-orphan")
    care_tips = relationship('CareTip', back_populates='plant', cascade="all, delete-orphan")
    categories = relationship('PlantCategory', back_populates='plant', cascade="all, delete-orphan")

class PlantName(Base):
    __tablename__ = 'plant_names'

    name_id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(String, ForeignKey('plants.plant_id'), nullable=True)
    name = Column(String(50), nullable=False)

    plant = relationship('Plant', back_populates='names')

Plant.names = relationship('PlantName', back_populates='plant', cascade="all, delete-orphan")



class CareTip(Base):
    __tablename__ = 'care_tips'

    plant_id = Column(String(100), ForeignKey('plants.plant_id'), primary_key=True)
    watering = Column(String(200))
    sunlight = Column(String(200))
    soil = Column(String(200))
    temp = Column(String(200))
    humidity = Column(String(200))
    common_issues = Column(String(200))

    plant = relationship('Plant', back_populates='care_tips')

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)

    plants = relationship('PlantCategory', back_populates='category', cascade="all, delete-orphan")

class PlantCategory(Base):
    __tablename__ = 'plant_categories'

    plant_id = Column(String(100), ForeignKey('plants.plant_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)

    plant = relationship('Plant', back_populates='categories')
    category = relationship('Category', back_populates='plants')
