from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from app import db
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    display_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    doctors = db.relationship("Doctor", backref="patient", cascade="delete")
    pharmacies = db.relationship("Pharmacy", backref="patient", cascade="delete")
    meds = db.relationship("Medication", backref="patient", cascade="delete")

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
        
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
    def doctor_list(self):
        my_doctors = Doctor.query.filter_by(user_id=self.id)
        return my_doctors.order_by(Doctor.doctor_last_name.collate('nocase').asc())
    
    def doctor_choices(self):
        my_doctors = self.doctor_list().all()
        doctor_choices = [(None, '')]
        for doctor in my_doctors:
            if doctor.doctor_first_name:
                doctor_name = doctor.doctor_first_name + " " + doctor.doctor_last_name
            else:
                doctor_name = doctor.doctor_last_name
            doctor_entry = (doctor.id, doctor_name)
            doctor_choices.append(doctor_entry)
        return doctor_choices
            
    def medication_list(self):
        my_meds = Medication.query.filter_by(user_id=self.id)
        return my_meds.order_by(Medication.medication_name.collate('nocase').asc())
    
    def medication_choices(self):
        my_medications = self.medication_list().all()
        medication_choices = []
        for medication in my_medications:
            medication_choices.append(medication.id)
        return medication_choices

    def pharmacy_list(self):
        my_pharmacies = Pharmacy.query.filter_by(user_id=self.id)
        return my_pharmacies.order_by(Pharmacy.pharmacy_name.collate('nocase').asc())

    def pharmacy_choices(self):
        my_pharmacies = self.pharmacy_list().all()
        pharmacy_choices = [(None, '')]
        for pharmacy in my_pharmacies:
            pharmacy_entry = (pharmacy.id, pharmacy.pharmacy_name)
            pharmacy_choices.append(pharmacy_entry)
        return pharmacy_choices
    
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
    medication_notes = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   

    def __repr__(self):
        return self.medication_name

    def prescribing_doctor_name(self):
        doctor_record = Doctor.query.filter_by(id=self.doctor_id).first_or_404()
        return doctor_record.full_name()

    def filling_pharmacy(self):
        pharmacy_record = Pharmacy.query.filter_by(id=self.pharmacy_id).first_or_404()
        return pharmacy_record.pharmacy_name    
    """I don't think I will need this, but let's wait to get everything working first
    def selected_doctor(self):
        if self.doctor_id:
            return (self.doctor_id, self.prescribing_doctor_name())
        else:
            return (None, "")"""

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_first_name = db.Column(db.String(64))
    doctor_last_name = db.Column(db.String(64))
    # for now only dealing with US addresses/phone numbers
    doctor_phone_number = db.Column(db.String(10))
    doctor_address_line_1 = db.Column(db.String(64))
    doctor_address_line_2 = db.Column(db.String(64))
    doctor_city = db.Column(db.String(64))
    doctor_state = db.Column(db.String(2))
    doctor_zipcode = db.Column(db.String(5))
    doctor_notes = db.Column(db.String(128))

    def __repr__(self):
        return 'Dr. {}'.format(self.doctor_last_name)

    def full_name(self):
        if self.doctor_first_name:
            doctor_name = self.doctor_first_name + " " + self.doctor_last_name
        else:
            doctor_name = self.doctor_last_name
        return doctor_name

class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pharmacy_name = db.Column(db.String(64))
    # for now only dealing with US addresses/phone numbers
    pharmacy_phone_number = db.Column(db.String(10))
    pharmacy_address_line_1 = db.Column(db.String(64))
    pharmacy_address_line_2 = db.Column(db.String(64))
    pharmacy_city = db.Column(db.String(64))
    pharmacy_state = db.Column(db.String(2))
    pharmacy_zipcode = db.Column(db.String(5))
    pharmacy_notes = db.Column(db.String(128))

    def __repr__(self):
        return self.pharmacy_name
