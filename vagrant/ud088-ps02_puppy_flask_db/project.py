from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, Adopter, PuppyProfile

import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# CRUD functionality for puppies
@app.route('/')
@app.route('/puppies/')
def puppy_list():
    # puppies = session.query(Puppy).order_by(Puppy.name)
    puppies = session.query(Puppy).order_by(Puppy.puppy_id)
    return render_template(
            'puppy_list.html', items = puppies)

@app.route('/puppies/<int:puppy_id>/')
def puppy_profile(puppy_id):
    puppy = session.query(Puppy).filter_by(puppy_id = puppy_id).one()
    return render_template(
            'puppy_profile.html', puppy = puppy)

@app.route('/puppies/new/', methods=['GET', 'POST'])
def puppy_new():
    if request.method == 'POST':
        newPuppy = Puppy(
                name = request.form['name'],
                dateOfBirth = datetime.datetime.strptime(
                    request.form['dateOfBirth'], "%Y-%m-%d").date(),
                gender = request.form['gender'],
                weight = request.form['weight']
                )
        session.add(newPuppy)
        session.commit()
        flash("New Puppy added!")
        return redirect(url_for('puppy_list'))
    else: # GET request
        return render_template('puppy_new.html')

@app.route('/puppies/<int:puppy_id>/edit/', methods=['GET', 'POST'])
def puppy_edit(puppy_id):
    puppy = session.query(Puppy).filter_by(puppy_id = puppy_id).one()
    if request.method == 'POST':
        if request.form['name']:
            puppy.name = request.form['name']
        if request.form['dateOfBirth']:
            puppy.dateOfBirth = datetime.datetime.strptime(
                    request.form['dateOfBirth'], "%Y-%m-%d").date()
        if request.form['gender']:
            puppy.gender = request.form['gender']
        if request.form['weight']:
            puppy.weight = request.form['weight']
        session.add(puppy)
        session.commit()
        flash("Puppy named " + puppy.name + " has been successfully edited.")
        return redirect(url_for('puppy_profile', \
                puppy_id = puppy_id))
    else: #GET request
        return render_template(
                'puppy_edit.html', puppy = puppy)

@app.route('/puppy/<int:puppy_id>/delete/', methods=['GET', 'POST'])
def puppy_delete(puppy_id):
    # TODO: implement delete functionality
    puppy = session.query(Puppy).filter_by(puppy_id = puppy_id).one()
    if request.method == 'POST':
        deleted_name = puppy.name
        session.delete(puppy)
        session.commit()
        flash("Puppy named " + deleted_name +
                " has been successfully deleted.")
        return redirect(url_for('puppy_list'))
    else:
        return render_template(
            'puppy_delete.html', puppy = puppy)

# End CRUD functionality for puppies




# CRUD functionality for shelters
@app.route('/shelters/')
def shelter_list():
    shelters = session.query(Shelter).order_by(Shelter.shelter_id)
    return render_template(
            'shelter_list.html', items = shelters)

@app.route('/shelters/<int:shelter_id>')
def shelter_profile(shelter_id):
    shelter = session.query(Shelter).filter_by(shelter_id = shelter_id).one()
    return render_template(
            'shelter_profile.html', shelter = shelter)

@app.route('/shelters/new/', methods=['GET', 'POST'])
def shelter_new():
    if request.method == 'POST':
        newShelter = Shelter(
                name = request.form['name'],
                address = request.form['address'],
                city = request.form['city'],
                state = request.form['state'],
                zipCode = request.form['zipCode'],
                website = request.form['website'],
                maximum_capacity = request.form['maximum_capacity'],
                current_occupancy = request.form['current_occupancy']
                )
        session.add(newShelter)
        session.commit()
        flash("New Shelter added!")
        return redirect(url_for('shelter_list'))
    else: # GET request
        return render_template('shelter_new.html')

@app.route('/shelters/<int:shelter_id>/edit/', methods=['GET', 'POST'])
def shelter_edit(shelter_id):
    shelter = session.query(Shelter).filter_by(shelter_id = shelter_id).one()
    if request.method == 'POST':
        # Begin check for edits
        if request.form['name']:
            shelter.name = request.form['name']
        if request.form['address']:
            shelter.address = request.form['address']
        if request.form['city']:
            shelter.city = request.form['city']
        if request.form['state']:
            shelter.state = request.form['state']
        if request.form['zipCode']:
            shelter.zipCode = request.form['zipCode']
        # End check for edits
        session.add(shelter)
        session.commit()
        flash("Shelter id number " + str(shelter.shelter_id) + " has been successfully edited.")
        return redirect(url_for('shelter_profile', \
                shelter_id = shelter_id))
    else: #GET request
        return render_template(
                'shelter_edit.html', shelter = shelter)

@app.route('/shelters/<int:shelter_id>/delete/', methods=['GET', 'POST'])
def shelter_delete(shelter_id):
    shelter = session.query(Shelter).filter_by(shelter_id = shelter_id).one()
    if request.method == 'POST':
        deleted_name = shelter.name
        deleted_id = str(shelter.shelter_id)
        session.delete(shelter)
        session.commit()
        flash("Shelter ID " + deleted_id + " has been deleted (" + \
                deleted_name + ").")
        return redirect(url_for('shelter_list'))
    else:
        return render_template(
                'shelter_delete.html', shelter = shelter)

# End CRUD functionality for shelters





# CRUD functionality for adopters
@app.route('/adopters/')
def adopter_list():
    adopters = session.query(Adopter).order_by(Adopter.adopter_id)
    return render_template(
            'adopter_list.html', items = adopters)

@app.route('/adopters/<int:adopter_id>')
def adopter_profile(adopter_id):
    adopter = session.query(Adopter).filter_by(adopter_id = adopter_id).one()
    return render_template(
            'adopter_profile.html', adopter = adopter)

@app.route('/adopters/new/', methods=['GET', 'POST'])
def adopter_new():
    if request.method == 'POST':
        newAdopter = Adopter(
                name = request.form['name'],
                # address = request.form['address'],
                # city = request.form['city'],
                # state = request.form['state'],
                # zipCode = request.form['zipCode'],
                # website = request.form['website'],
                # maximum_capacity = request.form['maximum_capacity'],
                # current_occupancy = request.form['current_occupancy']
                )
        session.add(newAdopter)
        session.commit()
        flash("New Adopter added!")
        return redirect(url_for('adopter_list'))
    else: # GET request
        return render_template('adopter_new.html')

@app.route('/adopters/<int:adopter_id>/edit/', methods = ['GET', 'POST'])
def adopter_edit(adopter_id):
    adopter = session.query(Adopter).filter_by(adopter_id = adopter_id).one()
    if request.method == 'POST':
        if request.form['name']:
            adopter.name = request.form['name']
        session.add(adopter)
        session.commit()
        flash("Adopter named " + str(adopter.name) + " has been successfully edited (id: " + str(adopter.adopter_id) + ")")
        return redirect(url_for('adopter_profile', adopter_id = adopter_id))
    else: # GET request
        return render_template(
                'adopter_edit.html', adopter = adopter)

@app.route('/adopters/<int:adopter_id>/delete/', methods = ['GET', 'POST'])
def adopter_delete(adopter_id):
    adopter = session.query(Adopter).filter_by(adopter_id = adopter_id).one()
    if request.method == 'POST':
        deleted_name = adopter.name
        deleted_id = str(adopter.adopter_id)
        session.delete(adopter)
        session.commit()
        flash("Adopter named " + deleted_name + " has been deleted (id: " + \
                deleted_id + ").")
        return redirect(url_for("adopter_list"))
    else:
        return render_template(
                'adopter_delete.html', adopter = adopter)

# End CRUD functionality for adopters






if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

