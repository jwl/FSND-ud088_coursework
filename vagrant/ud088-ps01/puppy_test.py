#!/usr/bin/env python
#
# Test cases for tournament.py

from database_setup import *
from puppy_functions import *

import puppypopulator_puppies

# ---------- Reference table from puppypopulator test data
# NOTE: shelter IDs are randomized everytime test data is generated!
    # >>> first_5_puppies()
    # name: Bailey,   id: 1,  shelter: 5
    # name: Max,      id: 2,  shelter: 3
    # name: Charlie,  id: 3,  shelter: 3
    # name: Buddy,    id: 4,  shelter: 5
    # name: Rocky,    id: 5,  shelter: 1
    # name: Jake,     id: 6,  shelter: 5
    # >>> first_5_shelters()
    # name: Oakland Animal Services
            # id: 1,
            # current occupancy: None
            # max capacity: None
    # name: San Francisco SPCA Mission Adoption Center
            # id: 2,
            # current occupancy: None
            # max capacity: None
    # name: Wonder Dog Rescue
            # id: 3,
            # current occupancy: None
            # max capacity: None
    # name: Humane Society of Alameda
            # id: 4,
            # current occupancy: None
            # max capacity: None
    # name: Palo Alto Humane Society
            # id: 5,
            # current occupancy: None
            # max capacity: None
# --------- End reference table


def setup():
    global transaction, connection, engine

    engine = create_engine('sqlite:///puppies.db')
    connection = engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(connection)


def teardown():
    transaction.rollback()
    connection.close()
    engine.dispose()


def test_check_in():
    # move puppy Bailey (puppy_id = 1) from shelter x to shelter x+1
    # if old shelter is 5, move to shelter 1

    test_puppy = session.query(Puppy).\
            filter(Puppy.puppy_id).first()
    old_shelter_id = test_puppy.shelter_id
    new_shelter_id = old_shelter_id % 5 + 1
    old_shelter = session.query(Shelter).\
            filter(Shelter.shelter_id == old_shelter_id).one()
    new_shelter = session.query(Shelter).\
            filter(Shelter.shelter_id == new_shelter_id).one()
    old_shelter_occupancy = old_shelter.current_occupancy
    new_shelter_occupancy = new_shelter.current_occupancy

    check_in(test_puppy.puppy_id, new_shelter_id)

    # Verify that puppy has a new shelter ID
    if test_puppy.shelter_id != new_shelter_id:
        raise ValueError(
                "\n\told_shelter_id is: " + str(old_shelter_id) +
                "\n\ttest_puppy.shelter_id: " + str(test_puppy.shelter_id) +
                "\n\tShelter ID for puppy should be " + str(new_shelter_id))
    # Verify that old shelter's occupancy has decremented
    if old_shelter.current_occupancy != (old_shelter_occupancy - 1):
        raise ValueError(
                "\n\told_shelter.current_occupancy is: " + \
                str(old_shelter.current_occupancy) +
                "\n\told_shelter_occupancy is: " + str(old_shelter_occupancy))
    # Verify that new shelter's occupancy has incremented
    if new_shelter.current_occupancy != (new_shelter_occupancy + 1):
        raise ValueError(
                "\n\tnew_shelter.current_occupancy is: " + \
                str(new_shelter.current_occupancy) +
                "\n\tnew_shelter_occupancy is: " + str(new_shelter_occupancy))
    print "1. Puppies can be checked-in and their old and new shelters" + \
            " have their occupancy values properly updated."


def test_adopt():
    adopters = session.query(Adopter).limit(2)
    adopter_ids = []
    for adopter in adopters:
        adopter_ids.extend([adopter.adopter_id])
    puppy = session.query(Puppy).\
            filter(Puppy.puppy_id == 1).one()
    old_shelter = session.query(Shelter).\
            filter(Shelter.shelter_id == puppy.shelter_id).one()
    old_shelter_occupancy = old_shelter.current_occupancy
    nami_puppies = adopters[0].puppies
    quinn_puppies = adopters[1].puppies

    # Print state of adopters and puppy before adoption
    # Nami and Quinn should each have an empty list for adopted puppies
    # Puppy's shelter should have occupancy of X
    # Puppy should have an empty list of adopters

    # for adopter in adopters:
        # print adopter.name + "'s adopted puppies: " + str(adopter.puppies)
    # print puppy.name + "'s adopters: " + str(puppy.adopters)
    # print old_shelter.name + "'s current occupancy is: " + \
            # str(old_shelter_occupancy)

    # adopt
    adopt(adopter_ids, puppy.puppy_id)

    # Reference database to find the newly changed Puppy
    new_puppy = session.query(Puppy).\
            filter(Puppy.puppy_id == 1).one()

    puppy_new_adopters = []
    for new_adopter in new_puppy.adopters:
        puppy_new_adopters.append(new_adopter.adopter_id)
    new_shelter_occupancy = old_shelter.current_occupancy

    # Verify that puppy has correct adopters referenced
    if len(new_puppy.adopters) != 2:
        raise ValueError(
                "\n\tPuppy: " + str(new_puppy.name) + " " + str(new_puppy.puppy_id) + \
                "\n\tIncorrect number of adopters: new_puppy.adopters: " + \
                        str(new_puppy.adopters))

    # Verify that adopters are the correct adopters
    for adopter in new_puppy.adopters:
        # print "Comparing " + str(adopter.adopter_id) + " to " + str(adopter_ids)
        if adopter.adopter_id not in adopter_ids:
            raise ValueError(
                    "\n\tIncorrect adopters listed: puppy.adopters: " + \
                            str(new_puppy.adopters))

    # Verify that adopters have puppy listed as adoptee
    for adopter in adopters:
        if adopter.adopter_id not in puppy_new_adopters:
            raise ValueError(
                    "\n\tadopter.adopter_id: " + str(adopter.adopter_id) + \
                    "\n\tnew_puppy_adopters: " + str(puppy_new_adopters))

    # Verify that shelter occupancy has been decremented
    if (old_shelter_occupancy - new_shelter_occupancy) != 1:
        raise ValueError(
                "\n\tShelter occupancy incorrectly updated: " + \
                        "old occupancy: " + str(old_shelter_occupancy) + \
                        "new occupancy: " + str(new_shelter_occupancy))

    # raise ValueError("test_adopt() is not yet implemented!")
    print "2. Puppies can be adopted."


if __name__ == '__main__':
    puppypopulator_puppies.populate_database()
    test_check_in()
    puppypopulator_puppies.populate_database()
    test_adopt()
    print "Success! All tests pass!"
