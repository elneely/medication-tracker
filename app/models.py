from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    display_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    doctors = db.relationship("Doctor", backref="user")
    pharmacies = db.relationship("Pharmacy", backref="user")
    meds = db.relationship("Medication", backref="user")
    # Not 100% sure I did the back_populates thing right here
 #   medications = db.relationship('Medication', back_populates='patient') 

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication_name = db.Column(db.String(128))
    brand_name = db.Column(db.String(64))
    dose = db.Column(db.String(64))
    frequency = db.Column(db.String((64)))
    prescription_date = db.Column(db.Date, index=True)
    last_filled = db.Column(db.Date, index=True)
    short_term = db.Column(db.Boolean)
    reminder = db.Column(db.Boolean, index=True)
    reminder_length = db.Column(db.Integer)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacy.id'))
    refills_remaining = db.Column(db.Integer, index=True)
    refills_expiration = db.Column(db.Date, index=True)
    length = db.Column(db.Integer, index=True)
    reason = db.Column(db.String(128))
    notes = db.Column(db.String(1024))
 #   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   

    def __repr__(self):
        return self.medication_name

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
  #  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    # for now only dealing with US addresses/phone numbers
    phone_number = db.Column(db.String(10))
    address_line_1 = db.Column(db.String(64))
    address_line_2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    notes = db.Column(db.String(128))

    def __repr__(self):
        return 'Dr. {}'.format(self.last_name)

class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
 #   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64))
    # for now only dealing with US addresses/phone numbers
    phone_number = db.Column(db.String(10))
    address_line_1 = db.Column(db.String(64))
    address_line_2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    notes = db.Column(db.String(128))

    def __repr__(self):
        return self.name
