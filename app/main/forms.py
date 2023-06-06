from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import BooleanField, DateField, EmailField, HiddenField, \
    IntegerField, RadioField, SelectField, SelectMultipleField, StringField, \
    SubmitField, TelField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, ValidationError, \
    Optional, NumberRange, Regexp
from wtforms.widgets import TextInput
from app.models import User, Doctor, Pharmacy, Medication

class EditProfileForm(FlaskForm):
    username = StringField(('Username'), validators=[DataRequired()])
    display_name = StringField('Display name')
    email = EmailField('Email address')
# make it possible to change password here?
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
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
    
class AddMedicationForm(FlaskForm):
    medication_name = StringField('Medication Name (Required): ', validators=[DataRequired(), Length(max=128)])
    brand_name = StringField('Brand name:', validators=[Length(max=64)])
    dose = StringField('Dosage: ', validators=[Length(max=64)])
    frequency = StringField('Frequency: ', validators=[Length(max=64)])
    prescription_date = DateField('Prescription Date: ', validators=[Optional()])
    last_filled = DateField('Last Filled: ', validators=[Optional()])
    short_term = BooleanField('Short term medication?')
    length = IntegerField('Length of prescription: ', widget=TextInput(), validators=[Optional()])
    reminder = BooleanField('Refill reminders on?')
    reminder_length = IntegerField('Please remind me ', widget=TextInput(), validators=[NumberRange(min=0, max=365),Optional()])   
    refills_remaining = IntegerField('Number of refills remaining: ', widget=TextInput(), validators=[NumberRange(min=0, max=30),Optional()])
    refills_expiration = DateField('Prescription expiration Date: ', validators=[Optional()])
    reason = StringField('Reason for taking: ', validators=[Length(max=128)])
    medication_notes = TextAreaField('Notes: ', validators=[Length(max=1024)])
    doctor_choice = RadioField('', choices=[('current-doctor', 'Current Doctor'), ('new-doctor', 'New Doctor')], default='current-doctor')
    doctor_list =  SelectField('Choose a doctor: ', validators=[Optional()])
    new_doctor_first = StringField('First Name: ', validators=[Length(max=64)])
    new_doctor_last = StringField('Last Name: ', validators=[Length(max=64)])
    pharmacy_choice = RadioField('', choices=[('current-pharmacy', 'Current Pharmacy'), ('new-pharmacy', 'New Pharmacy')], default='current-pharmacy')
    pharmacy_list = SelectField('Choose a pharmacy: ', validators=[Optional()]) 
    new_pharmacy_name = StringField('Pharmacy Name: ', validators=[Length(max=64)])
    submit = SubmitField('Submit')
    
    def validate_new_doctor_last(self, new_doctor_last):
        if new_doctor_last.data is not None:  
            name = Doctor.query.filter_by(user_id=current_user.id, doctor_first_name=self.new_doctor_first.data, doctor_last_name=new_doctor_last.data).first()
            if name is not None:
                raise ValidationError("You already have a doctor with this name")

    def validate_new_pharmacy_name(self, new_pharmacy_name):
        if new_pharmacy_name.data is not None:
            name = Pharmacy.query.filter_by(user_id=current_user.id, pharmacy_name=self.new_pharmacy_name.data).first()
            if name is not None:
                raise ValidationError("You already have a pharmacy with this name")

class EditMedicationForm(FlaskForm):
    medication_name = StringField('Medication Name (Required): ', validators=[DataRequired(), Length(max=128)])
    brand_name = StringField('Brand name:', validators=[Length(max=64)])
    dose = StringField('Dosage: ', validators=[Length(max=64)])
    frequency = StringField('Frequency: ', validators=[Length(max=64)])
    prescription_date = DateField('Prescription Date: ', validators=[Optional()])
    last_filled = DateField('Last Filled: ', validators=[Optional()])
    short_term = BooleanField('Short term medication?')
    length = IntegerField('Length of prescription: ', widget=TextInput(), validators=[Optional()])
    reminder = BooleanField('Refill reminders on?')
    reminder_length = IntegerField('Please remind me ', widget=TextInput(), validators=[NumberRange(min=0, max=365),Optional()])   
    refills_remaining = IntegerField('Number of refills remaining: ', widget=TextInput(), validators=[NumberRange(min=0, max=30),Optional()])
    refills_expiration = DateField('Prescription expiration Date: ', validators=[Optional()])
    reason = StringField('Reason for taking: ', validators=[Length(max=128)])
    medication_notes = TextAreaField('Notes: ', validators=[Length(max=1024)])
    doctor_list =  SelectField('Doctor: ', validators=[Optional()])
    pharmacy_list = SelectField('Pharmacy: ', validators=[Optional()]) 
    submit = SubmitField('Submit')

    def __init__(self, original_name, *args, **kwargs):
        super(EditMedicationForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        
class ManageMedicationsForm(FlaskForm):
    action_choice = SelectField('Action:', choices=[('default', 'Please select'), ('change-doctor', 'Change Doctor'), ('change-pharmacy', 'Change Pharmacy'), ('delete-medication', 'Delete Medication')], default="default")
    doctor_list =  SelectField('Doctor: ', validators=[Optional()])
    pharmacy_list = SelectField('Pharmacy: ', validators=[Optional()]) 
    delete_confirmation = RadioField('Are you certain you wish to delete these medications?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    selected_medications = SelectMultipleField('Select Medications', coerce=int)
    submit = SubmitField('Submit')

    def validate_action_choice(self, action_choice):
        if action_choice.data == "default":
            raise ValidationError("You have not chosen an action.")


class AddDoctorForm(FlaskForm):
    doctor_first_name = StringField('First name (optional)', validators=[Length(max=64)])
    doctor_last_name = StringField('Last name', validators=[DataRequired(), Length(max=64)])
    doctor_phone_number = TelField('Telephone number') #not sure I have this input working with model
    doctor_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    doctor_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    doctor_city = StringField('City', validators=[Length(max=64)])
    doctor_state = StringField('State', validators=[Length(max=2)])
    doctor_zipcode = StringField('Zipcode', validators=[Length(max=5)])
    doctor_notes = TextAreaField('Notes', validators=[Length(max=128)])
    referring_URL = HiddenField()
    submit = SubmitField('Submit')

    def validate_doctor_last_name(self, doctor_last_name):
        name = Doctor.query.filter_by(user_id=current_user.id, doctor_first_name=self.doctor_first_name.data, doctor_last_name=doctor_last_name.data).first()
        if name is not None:
            raise ValidationError("You already have a doctor with this name")

   # def validate_referring_URL(self, referring_URL):


class EditDoctorForm(FlaskForm):
    doctor_first_name = StringField('First name (optional)', validators=[Length(max=64)])
    doctor_last_name = StringField('Last name', validators=[DataRequired(), Length(max=64)])
    doctor_phone_number = TelField('Telephone number') #not sure I have this input working with model
    doctor_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    doctor_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    doctor_city = StringField('City', validators=[Length(max=64)])
    doctor_state = StringField('State', validators=[Length(max=2)])
    doctor_zipcode = StringField('Zipcode', validators=[Length(max=5)])
    doctor_notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')

    def __init__(self, original_full_name, *args, **kwargs):
        super(EditDoctorForm, self).__init__(*args, **kwargs)
        self.original_full_name = original_full_name

    def validate_doctor_last_name(self, doctor_last_name):
        if self.doctor_first_name.data:
            doctor_name = self.doctor_first_name.data + " " + doctor_last_name.data
        else:
            doctor_name = doctor_last_name.data

        if doctor_name != self.original_full_name:
            name = Doctor.query.filter_by(user_id=current_user.id, doctor_first_name=self.doctor_first_name.data, doctor_last_name=doctor_last_name.data).first()
            if name is not None:
                raise ValidationError("You already have a doctor with this name")
        


class AddPharmacyForm(FlaskForm):
    pharmacy_name = StringField('Name of Pharmacy', validators=[Length(max=64), DataRequired()])
    pharmacy_phone_number = TelField('Telephone number') #not sure I have this input working with model
    pharmacy_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    pharmacy_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    pharmacy_city = StringField('City', validators=[Length(max=64)])
    pharmacy_state = StringField('State', validators=[Length(max=2)])
    pharmacy_zipcode = StringField('Zipcode', validators=[Length(max=5)])
    pharmacy_notes = TextAreaField('Notes', validators=[Length(max=128)])
    referring_URL = HiddenField()
    submit = SubmitField('Submit')
# not sure that last part works
    def validate_pharmacy_name(self, pharmacy_name):
        check_name = Pharmacy.query.filter_by(user_id=current_user.id, pharmacy_name=pharmacy_name.data).first()
        if check_name is not None:
            raise ValidationError("You already have a pharmacy with this name.")
        if pharmacy_name.data.isspace() == True:
            raise ValidationError("You cannot leave a blank name.")


class EditPharmacyForm(FlaskForm):
    pharmacy_name = StringField('Name of Pharmacy', validators=[Length(max=64), DataRequired()])
    pharmacy_phone_number = TelField('Telephone number') #not sure I have this input working with model
    pharmacy_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    pharmacy_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    pharmacy_city = StringField('City', validators=[Length(max=64)])
    pharmacy_state = StringField('State', validators=[Length(max=2)])
    pharmacy_zipcode = StringField('Zipcode', validators=[Length(max=5)])
    pharmacy_notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')

    def __init__(self, original_name, *args, **kwargs):
        super(EditPharmacyForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
# not sure that last part works
    def validate_pharmacy_name(self, pharmacy_name):
        if pharmacy_name.data.isspace() == True:
            raise ValidationError("You cannot leave a blank name.")
        if pharmacy_name.data != self.original_name:
            check_name = Pharmacy.query.filter_by(user_id=current_user.id, pharmacy_name=pharmacy_name.data).first()
            if check_name is not None:
                raise ValidationError("You already have a pharmacy with this name.")

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class DeleteProfileForm(FlaskForm):
    delete_confirmation = RadioField('Are you certain you wish to delete your account?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    extra_confirmation = RadioField('There is no undoing this action - are you completely certain?', choices=[('certain-no', 'No'), ('certain-yes', 'Yes')], default='certain-no')
    submit = SubmitField('Permanently delete this account')
    
class DeleteDoctorForm(FlaskForm):
    referring_URL = HiddenField()
    delete_confirmation = RadioField('Are you certain you wish to delete this doctor?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    submit = SubmitField('Permanently delete this doctor')

class DeletePharmacyForm(FlaskForm):
    referring_URL = HiddenField()
    delete_confirmation = RadioField('Are you certain you wish to delete this pharmacy?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    submit = SubmitField('Permanently delete this pharmacy')