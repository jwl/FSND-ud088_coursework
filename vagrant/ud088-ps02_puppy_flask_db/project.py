from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, Adopter, PuppyProfile

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
            'puppy_list.html', puppies = puppies)

@app.route('/puppies/<int:puppy_id>')
def puppyProfile(puppy_id):
    print "puppyProfile, puppy_id: ", puppy_id
    puppy = session.query(Puppy).filter_by(puppy_id = puppy_id).one()
    return render_template(
            'puppy_profile.html', puppy = puppy)

@app.route('/puppies/<int:puppy_id>/new/', methods=['GET', 'POST'])
def newPuppy(puppy_id):
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



# CRUD functionality for shelters
@app.route('/shelters/')
def shelter_list():
    shelters = session.query(Shelter).order_by(Shelter.shelter_id)
    return render_template(
            'shelter_list.html', items = shelters)



# CRUD functionality for adopters
@app.route('/adopters/')
def adopter_list():
    adopters = session.query(Adopter).order_by(Adopter.adopter_id)
    return render_template(
            'adopter_list.html', items = adopters)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

