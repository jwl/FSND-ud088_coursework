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

@app.route('/puppies/<int:puppy_id>')
def puppy_profile(puppy_id):
    puppy = session.query(Puppy).filter_by(puppy_id = puppy_id).one()
    return render_template(
            'puppy_profile.html', puppy = puppy)

@app.route('/puppies/<int:puppy_id>/new/', methods=['GET', 'POST'])
def puppy_new(puppy_id):
    if request.method == 'POST':
        newPuppy = Puppy(
                # name = request.form['name'], restaurant_id = restaurant_id
                )
        session.add(newPuppy)
        session.commit()
        flash("New Puppy added!")
        return redirect(url_for('puppy_list'))
    else: # GET request
        return render_template('new_puppy.html', \
                puppy_id = puppy_id)

@app.route('/puppies/<int:puppy_id>/edit/', methods=['GET', 'POST'])
def puppy_edit(puppy_id):
    puppy = session.query(Puppy).filter_by(puppy_id = puppy_id).one()
    if request.method == 'POST':
        if request.form['name']:
            puppy.name = request.form['name']
        if request.form['dateOfBirth']:
            puppy.dateOfBirth = datetime.datetime.strptime(request.form['dateOfBirth'], "%Y-%m-%d").date()
        if request.form['gender']:
            puppy.gender = request.form['gender']
        if request.form['weight']:
            puppy.weight = request.form['weight']
        # if request.form['description']:
            # puppy.profile.description = request.form['description']
            # session.add(puppy.profile)
        # if request.form['specialNeeds']:
            # puppy.profile.specialNeeds = request.form['specialNeeds']
            # session.add(puppy.profile)
        session.add(puppy)
        session.commit()
        flash("Puppy named " + puppy.name + " has been successfully edited.")
        return redirect(url_for('puppy_profile', \
                puppy_id = puppy_id))
    else: #GET request
        return render_template(
                'puppy_edit.html', puppy = puppy)

@app.route('/puppy/<int:puppy_id>/delete/')
def puppy_delete(puppy_id):
    # TODO: implement delete functionality
    puppy = session.query(Puppy).filter_by(puppy_id = puppy_id).one()
    return render_template(
            'puppy_profile.html', puppy = puppy)

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

@app.route('/shelters/<int:shelter_id>/edit/')
def shelter_edit(shelter_id):
    # TODO: implement edit functionality
    shelter = session.query(Shelter).filter_by(shelter_id = shelter_id).one()
    return render_template(
            'shelter_profile.html', shelter = shelter)

@app.route('/shelters/<int:shelter_id>/delete/')
def shelter_delete(shelter_id):
    # TODO: implement delete functionality
    shelter = session.query(Shelter).filter_by(shelter_id = shelter_id).one()
    return render_template(
            'shelter_profile.html', shelter = shelter)

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

@app.route('/adopters/<int:adopter_id>/edit/')
def adopter_edit(adopter_id):
    # TODO: implement edit functionality
    adopter = session.query(Adopter).filter_by(adopter_id = adopter_id).one()
    return render_template(
            'adopter_profile.html', adopter = adopter)

@app.route('/adopters/<int:adopter_id>/delete/')
def adopter_delete(adopter_id):
    # TODO: implement delete functionality
    adopter = session.query(Adopter).filter_by(adopter_id = adopter_id).one()
    return render_template(
            'adopter_profile.html', adopter = adopter)

# End CRUD functionality for adopters






if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

