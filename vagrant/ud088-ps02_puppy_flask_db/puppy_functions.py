from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy, Adopter, PuppyProfile

import datetime

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def ex02_queries():
    # ========== Exercise 2 queries
    # 1. Query all the puppies, return results in ascending alphabetical order
    print "Query all the puppies, return results in ascending alphabetical order"
    list_of_puppies = session.query(Puppy).order_by(Puppy.name)
    for puppy in list_of_puppies:
        print puppy.name


    # 2. Query all puppies less than 6 months old, order by youngest first
    print "Query all puppies less than 6 months old, order by youngest first"
    today = datetime.date.today()
    # six months is approx 183 days
    six_months_ago = today - datetime.timedelta(183)
    youngest_puppies = session.query(Puppy).filter(
            Puppy.dateOfBirth >= six_months_ago).order_by(desc(
                Puppy.dateOfBirth))
    for puppy in youngest_puppies:
        print puppy.name, puppy.dateOfBirth


    # 3. Query all puppies by ascending weight
    print "Query all puppies by ascending weight"
    puppies_by_weight = session.query(Puppy).\
            order_by(Puppy.weight)
    for puppy in puppies_by_weight:
        print puppy.name, puppy.weight


    # 4. Query all puppies grouped by their shelter
    print "Query all puppies grouped by their shelter"
    puppies_by_shelter = session.query(Puppy).\
            order_by(Puppy.shelter_id)
    for puppy in puppies_by_shelter:
        print puppy.name, puppy.shelter_id

    # ========== End Exercise 2 queries

# uncomment to execute exercise 2 queries
# ex02_queries()

def first_5_puppies():
    i = 0
    first_five = session.query(Puppy)
    for puppy in first_five:
        print "name: " + puppy.name + ",\tid: " + str(puppy.puppy_id) + ",\tshelter: " + str(puppy.shelter_id)
        if i > 5:
            break
        i += 1


def first_5_shelters():
    i = 0
    first_five = session.query(Shelter)
    for shelter in first_five:
        print "name: " + shelter.name + "\n\tid: " + str(shelter.shelter_id) + "\n\tcurrent occupancy: " + str(shelter.current_occupancy) + "\n\tmax capacity: " + str(shelter.maximum_capacity)
        if i > 5:
            break
        i += 1


def check_in(puppy_id, shelter_id):
    """ Assigns a given puppy to a given shelter, provided there is capacity.

    Takes puppy id, and provided sufficient capacity exists at shelter
    indicated by shelter, assigns it to that shelter. If capacity at shelter
    is insufficient, prints an error message and makes no changes to
    the database.

    Args:
      puppy_id: (Integer) ID number of puppy
      shelter_id: (Integer) ID number of shelter
    """
    shelter = session.query(Shelter).\
            filter(Shelter.shelter_id == shelter_id).one()
    if (shelter.current_occupancy >= shelter.maximum_capacity):
        print "Try another shelter"
    else:
        puppy = session.query(Puppy).\
                filter(Puppy.puppy_id == puppy_id).one()
        # print "Assigning puppy " + str(puppy_id) + " with old shelter id " + \
                # str(puppy.shelter_id)  + " to shelter " + str(shelter_id)
        if (puppy.shelter_id):
            # If the puppy was already at a shelter,
            # remove it and decrement the current occupancy
            old_shelter = session.query(Shelter).\
                    filter(Shelter.shelter_id == puppy.shelter_id).one()
            old_shelter.current_occupancy -= 1
            session.add(old_shelter)
            session.commit()
        # Increment the current occupancy at the new shelter
        # and assign the new shelter id to the puppy
        shelter.current_occupancy += 1
        puppy.shelter_id = shelter_id
        # Commit changes
        # print "puppy's new shelter id is: " + str(puppy.shelter_id)
        session.add(puppy)
        session.commit()
        session.add(shelter)
        session.commit()


def adopt(adopter_ids, puppy_id):
    """ Create a method for adopting a puppy based on its id.

    The method should also take in an array of adopter ids of the family
    members who will be responsible for the puppy. An adopted puppy
    should stay in the puppy database but no longer be taking up an occupancy
    spot in the shelter.

    Args:
      adopters: array of adopter IDs
      puppy_id: ID of puppy that is being adopted
    """
    # print "adopters: " + str(adopters)
    # print "puppy_id: " + str(puppy_id)
    # TODO
    puppy = session.query(Puppy).\
            filter(Puppy.puppy_id == puppy_id).one()
    adopters = []

    # Lookup adopters corresponding to adopter IDs and store in list
    for adopter_id in adopter_ids:
        adopters.append(session.query(Adopter).\
                filter(Adopter.adopter_id == adopter_id).one())
    # print puppy
    # print adopters

    # Add adopters to puppy
    for adopter in adopters:
        puppy.adopters.append(adopter)

    if puppy.shelter_id:
        shelter = session.query(Shelter).\
                filter(Shelter.shelter_id == puppy.shelter_id).one()
        puppy.shelter_id = None
        shelter.current_occupancy -= 1
        session.add(shelter)

    session.add(puppy)
    for adopter in adopters:
        session.add(adopter)
    session.commit()

