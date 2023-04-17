from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, EmailField, HiddenField, \
    IntegerField, StringField, SubmitField, TelField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, NumberRange, Regexp
from wtforms.widgets import TextInput

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
    medication_name = StringField('Medication Name', validators=[DataRequired(), Length(max=128)])
    brand_name = StringField('Brand name (optional)', validators=[Length(max=64)])
    dose = StringField('Dosage', validators=[Length(max=64)])
    frequency = StringField('Frequency', validators=[Length(max=64)])
    prescription_date = DateField('Prescription Date', format='%m/%d/%Y', validators=[Optional()])
    last_filled = DateField('Last Filled', format='%m/%d/%Y', validators=[Optional()])
    short_term = BooleanField('Short term medication?')
    length = IntegerField('Length of prescription?', widget=TextInput(), validators=[Optional()])
    reminder = BooleanField('Refill reminders on?')
    reminder_length = IntegerField('How many days in advance do you want to be reminded?', widget=TextInput(), validators=[NumberRange(min=0, max=365),Optional()])
    doctor_id = HiddenField('Prescribing doctor')
    pharmacy_id = HiddenField('Pharmacy')
    doctor_first_name = StringField('First name', validators=[Length(max=64)])
    doctor_last_name = StringField('Last name', validators=[Length(max=64)])
    pharmacy_name = StringField('Pharmacy name', validators=[Length(max=64)])
    refills_remaining = IntegerField('Number of refills remaining', widget=TextInput(), validators=[NumberRange(min=0, max=30),Optional()])
    refills_expiration = DateField('Expiration Date', format='%m/%d/%Y', validators=[Optional()])
    reason = StringField('Reason for taking', validators=[Length(max=128)])
    notes = TextAreaField('Notes', validators=[Length(max=1024)])
    submit = SubmitField('Submit')

 #   def __init__(self, username):
 #       self.id = 

    
class DoctorForm(FlaskForm):
    first_name = StringField('First name (optional)', validators=[Length(max=64)])
    last_name = StringField('Last name', validators=[Length(max=64), DataRequired()])
    phone_number = TelField('Telephone number') #not sure I have this input working with model
    address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    city = StringField('City', validators=[Length(max=64)])
    state = StringField('State', validators=[Length(max=2)])
    zipcode = StringField('Zipcode', validators=[Length(max=5)])
    notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')


class PharmacyForm(FlaskForm):
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