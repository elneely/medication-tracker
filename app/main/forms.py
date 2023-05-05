from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import BooleanField, DateField, EmailField, HiddenField, \
    IntegerField, SelectField, StringField, SubmitField, TelField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, NumberRange, Regexp
from wtforms.widgets import TextInput
from app.models import User, Doctor

class ProfileForm(FlaskForm):
    username = StringField(('Username'), validators=[DataRequired()])
    display_name = StringField('Display name')
    email = EmailField('Email address')
# make it possible to change password here?
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(('Please use a different username.'))
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')
    
class MedicationForm(FlaskForm):
    medication_name = StringField('Medication Name (Required): ', validators=[DataRequired(), Length(max=128)])
    brand_name = StringField('Brand name:', validators=[Length(max=64)])
    dose = StringField('Dosage: ', validators=[Length(max=64)])
    frequency = StringField('Frequency: ', validators=[Length(max=64)])
    prescription_date = DateField('Prescription Date: ', format='%m/%d/%Y', validators=[Optional()])
    last_filled = DateField('Last Filled: ', format='%m/%d/%Y', validators=[Optional()])
    short_term = BooleanField('Short term medication?')
    length = IntegerField('Length of prescription: ', widget=TextInput(), validators=[Optional()])
    reminder = BooleanField('Refill reminders on?')
    reminder_length = IntegerField('Please remind me ', widget=TextInput(), validators=[NumberRange(min=0, max=365),Optional()])
    doctor_list =  SelectField('Choose a doctor: ', )
    pharmacy_id = HiddenField('Pharmacy: ') 
    refills_remaining = IntegerField('Number of refills remaining: ', widget=TextInput(), validators=[NumberRange(min=0, max=30),Optional()])
    refills_expiration = DateField('Prescription expiration Date: ', format='%m/%d/%Y', validators=[Optional()])
    reason = StringField('Reason for taking: ', validators=[Length(max=128)])
    notes = TextAreaField('Notes: ', validators=[Length(max=1024)])
    new_doctor_first = StringField('First Name: ', validators=[Length(max=64)])
    new_doctor_last = StringField('Last Name (Required): ', validators=[Length(max=64)])
    submit = SubmitField('Submit')
    
    def validate_new_doctor_last(self, new_doctor_last):
        if new_doctor_last.data:  
            name = Doctor.query.filter_by(user_id=current_user.id, first_name=self.new_doctor_first.data, last_name=new_doctor_last.data).first()
            if name is not None:
                raise ValidationError("You already have a doctor with this name")

class AddDoctorForm(FlaskForm):
    first_name = StringField('First name (optional)', validators=[Length(max=64)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=64)])
    phone_number = TelField('Telephone number') #not sure I have this input working with model
    address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    city = StringField('City', validators=[Length(max=64)])
    state = StringField('State', validators=[Length(max=2)])
    zipcode = StringField('Zipcode', validators=[Length(max=5)])
    notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')

    def validate_last_name(self, last_name):
        name = Doctor.query.filter_by(user_id=current_user.id, first_name=self.first_name.data, last_name=last_name.data).first()
        if name is not None:
            raise ValidationError("You already have a doctor with this name")
     
class AddPharmacyForm(FlaskForm):
    name = StringField('Name of Pharmacy', validators=[Length(max=64), DataRequired()])
    phone_number = TelField('Telephone number') #not sure I have this input working with model
    address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    city = StringField('City', validators=[Length(max=64)])
    state = StringField('State', validators=[Length(max=2)])
    zipcode = StringField('Zipcode', validators=[Length(max=5)])
    notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')