from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column(String(80), nullable = False)
    address = Column(String(80), nullable = False)
    city = Column(String(80), nullable = False)
    state = Column(String(80), nullable = False)
    zipCode = Column(String(5), nullable = False)
    website = Column(String(250), nullable = False)
    shelter_id = Column(Integer, primary_key = True)
    maximum_capacity = Column(Integer)
    current_occupancy = Column(Integer)

    def getMaximumCapcity(self):
        return self.maximum_capacity

    def setMaximumCapacity(self, value):
        self.maximum_capacity = value

    def getCurrentOccupancy(self):
        return self.current_occupancy

    def setCurrentOccupancy(self, value):
        self.current_occupancy = value

puppy_adopter_table = Table('puppy_adopter', Base.metadata,
        Column('puppy_id', Integer, ForeignKey('puppy.puppy_id')),
        Column('adopter_id', Integer, ForeignKey('adopter.adopter_id'))
)

class Puppy(Base):
    __tablename__ = 'puppy'
    puppy_id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    dateOfBirth = Column(Date)
    gender = Column(String(6), nullable = False)
    weight = Column(Integer)
    shelter_id = Column(Integer, ForeignKey('shelter.shelter_id'))
    picture = Column(String)
    shelter = relationship(Shelter)
    profile = relationship("PuppyProfile", uselist = False,
            backref="puppy")
    adopters = relationship("Adopter",
            secondary = puppy_adopter_table, backref = "puppies")

class Adopter(Base):
    __tablename__ = 'adopter'
    adopter_id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

class PuppyProfile(Base):
    __tablename__ = 'puppyprofile'
    profile_id = Column(Integer, ForeignKey('puppy.puppy_id'), primary_key = True)
    photoURL = Column(String(250))
    description = Column(String(1024))
    specialNeeds = Column(String(1024))




engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)
