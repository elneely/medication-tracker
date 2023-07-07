from datetime import datetime
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import BooleanField, DateField, EmailField, \
    IntegerField, RadioField, SelectField, SelectMultipleField, StringField, \
    SubmitField, TelField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, \
    Optional, NumberRange, Regexp
from wtforms.widgets import TextInput
from app.models import User, Doctor, Pharmacy 
from app.main.select_options import states

class EditProfileForm(FlaskForm):
    """A form for editing a user's profile"""
    username = StringField(('Username'), validators=[DataRequired()])
    display_name = StringField('Display name')
    email = EmailField('Email address')
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        # Check username is unique, not blank, and alphanumeric
        if username.data.lower() != self.original_username:
            user = User.query.filter_by(username=self.username.data.lower()).first()
            if user is not None:
                raise ValidationError('Please use a different username')
            elif username.data.isspace() == True:
                raise ValidationError('Usernames cannot be blank')
            elif username.data.isalnum() == False:
                raise ValidationError('Usernames can only contain letters and numbers')
    
    def validate_email(self, email):
        # Check email is unique
        if email.data.lower() != self.original_email:
            user = User.query.filter_by(email=self.email.data.lower()).first()
            if user is not None:
                raise ValidationError('Please use a different email.')
    
class AddMedicationForm(FlaskForm):
    """A form for adding medications"""
    medication_name = StringField('Medication Name (Required): ', validators=[DataRequired(), Length(max=128)])
    brand_name = StringField('Brand name:', validators=[Length(max=64)])
    dose = StringField('Dosage: ', validators=[Length(max=64)])
    frequency = StringField('Frequency: ', validators=[Length(max=64)])
    prescription_date = DateField('Prescription Date: ', validators=[Optional()])
    last_filled = DateField('Last Filled: ', validators=[Optional()])
    short_term = BooleanField('Short-term medication?')
    length = IntegerField('Length of prescription: ', widget=TextInput(), validators=[Optional()])
    reminder = BooleanField('Refill reminders on?')
    reminder_length = IntegerField('Please remind me ', widget=TextInput(), validators=[NumberRange(min=0, max=365),Optional()])   
    refills_remaining = IntegerField('Number of refills remaining: ', widget=TextInput(), validators=[Optional()])
    refills_expiration = DateField('Prescription Expiration Date: ', validators=[Optional()])
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
    
    def validate_medication_name(self, medication_name):
        # Check medication name is not blank
        if medication_name.data.isspace() == True:
            raise ValidationError('Medication names cannot be blank')
        
    def validate_prescription_date(self, prescription_date):
        # Check prescription date is not in the future
        present = datetime.now()
        if prescription_date.data > present.date():
            raise ValidationError('Prescription date cannot be in the future')
        
    def validate_refills_expiration(self, refills_expiration):
        # Check that refill expiration date is after the present date and the 
        # prescription date
        present = datetime.now()
        if refills_expiration.data < present.date():
            raise ValidationError('This date has already passed')
        if self.prescription_date.data and (self.prescription_date.data > refills_expiration.data):
            raise ValidationError('Prescription cannot expire before it is prescribed')
    
    def validate_last_filled(self, last_filled):
        # Check that last filled date is not in the future, not before it was prescribed
        # and not after it expires
        present = datetime.now()
        if last_filled.data > present.date():
            raise ValidationError('Cannot enter future date')
        if self.prescription_date.data and (self.prescription_date.data > last_filled.data):
            raise ValidationError('You cannot fill a prescription before it is prescribed')
        if self.refills_expiration.data and (self.refills_expiration.data < last_filled.data):
            raise ValidationError('You cannot fill a prescription after it has expired')
    
    def validate_length(self, length):
        # Check prescription length is at least 1 day
        if length.data <= 0:
            raise ValidationError('Prescription must be for at least one day')
    
    def validate_refills_remaining(self, refills_remaining):
        # Check that there are a non-negative number of refills remaining
        if refills_remaining.data < 0:
            raise ValidationError('You cannot have a negative number of refills')
    
    def validate_reminder(self, reminder):
        # If they say they want reminders, check that they have also set a reminder
        # length, prescription length, and last filled date
        if reminder.data == True:
            if (self.reminder_length.data or self.length.data or self.last_filled.data) is None:
                raise ValidationError('You must set a reminder length, prescription length, and last filled date')

    def validate_reminder_length(self, reminder_length):
        # Check that reminder length is not longer than prescription length
        if self.length.data and (reminder_length.data > self.length.data):
            raise ValidationError('Reminder length cannot be longer than the length of the prescription')

    def validate_new_doctor_last(self, new_doctor_last):
        # Check the doctor has a unique name
        if new_doctor_last.data is not None:  
            name = Doctor.query.filter_by(user_id=current_user.id, doctor_first_name=self.new_doctor_first.data, doctor_last_name=new_doctor_last.data).first()
            if name is not None:
                raise ValidationError("You already have a doctor with this name")

    def validate_new_pharmacy_name(self, new_pharmacy_name):
        # Check the pharmacy has a unique name
        if new_pharmacy_name.data is not None:
            name = Pharmacy.query.filter_by(user_id=current_user.id, pharmacy_name=self.new_pharmacy_name.data).first()
            if name is not None:
                raise ValidationError("You already have a pharmacy with this name")

class EditMedicationForm(FlaskForm):
    """A form for editing medication information"""
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

    def validate_medication_name(self, medication_name):
        # Check medication name is not blank
        if medication_name.data.isspace() == True:
            raise ValidationError('Medication names cannot be blank')
        
    def validate_prescription_date(self, prescription_date):
        # Check prescription date is not in the future
        present = datetime.now()
        if prescription_date.data > present.date():
            raise ValidationError('Prescription date cannot be in the future')
        
    def validate_refills_expiration(self, refills_expiration):
        # Check that refill expiration date is after the present date and the 
        # prescription date
        present = datetime.now()
        if refills_expiration.data < present.date():
            raise ValidationError('This date has already passed')
        if self.prescription_date.data and (self.prescription_date.data > refills_expiration.data):
            raise ValidationError('Prescription cannot expire before it is prescribed')
    
    def validate_last_filled(self, last_filled):
        # Check that last filled date is not in the future, not before it was prescribed
        # and not after it expires
        present = datetime.now()
        if last_filled.data > present.date():
            raise ValidationError('Cannot enter future date')
        if self.prescription_date.data and (self.prescription_date.data > last_filled.data):
            raise ValidationError('You cannot fill a prescription before it is prescribed')
        if self.refills_expiration.data and (self.refills_expiration.data < last_filled.data):
            raise ValidationError('You cannot fill a prescription after it has expired')
    
    def validate_length(self, length):
        # Check prescription length is at least 1 day
        if length.data <= 0:
            raise ValidationError('Prescription must be for at least one day')
    
    def validate_refills_remaining(self, refills_remaining):
        # Check that there are a non-negative number of refills remaining
        if refills_remaining.data < 0:
            raise ValidationError('You cannot have a negative number of refills')
    
    def validate_reminder(self, reminder):
        # If they say they want reminders, check that they have also set a reminder
        # length, prescription length, and last filled date
        if reminder.data == True:
            if (self.reminder_length.data or self.length.data or self.last_filled.data) is None:
                raise ValidationError('You must set a reminder length, prescription length, and last filled date')

    def validate_reminder_length(self, reminder_length):
        # Check that reminder length is not longer than prescription length
        if self.length.data and (reminder_length.data > self.length.data):
            raise ValidationError('Reminder length cannot be longer than the length of the prescription')


class ManageMedicationsForm(FlaskForm):
    """A form for performing bulk actions on medications"""
    action_choice = SelectField('Action:', choices=[('default', 'Please select'), ('change-doctor', 'Change Doctor'), ('change-pharmacy', 'Change Pharmacy'), ('delete-medication', 'Delete Medication')], default="default")
    doctor_list =  SelectField('Doctor: ', validators=[Optional()])
    pharmacy_list = SelectField('Pharmacy: ', validators=[Optional()]) 
    delete_confirmation = RadioField('Are you certain you wish to delete these medications?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    selected_medications = SelectMultipleField('Select Medications', coerce=int)
    submit = SubmitField('Submit')

    def validate_action_choice(self, action_choice):
        # Checks to ensure at least one medication is selected
        if action_choice.data == "default":
            raise ValidationError("You have not chosen an action.") 


class AddDoctorForm(FlaskForm):
    """A form for adding a doctor"""
    doctor_first_name = StringField('First name (optional)', validators=[Length(max=64)])
    doctor_last_name = StringField('Last name', validators=[DataRequired(), Length(max=64)])
    doctor_phone_number = TelField('Telephone number', validators=[Optional(), Regexp(regex="^[0-9]{3}-[0-9]{3}-[0-9]{4}$", message="Valid format is xxx-xxx-xxxx")])
    doctor_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    doctor_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    doctor_city = StringField('City', validators=[Length(max=64)])
    doctor_state = SelectField('State', validators=[Optional()], choices=states)
    doctor_zipcode = StringField('Zipcode', validators=[Length(max=5), Optional()])
    doctor_notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')

    def validate_doctor_last_name(self, doctor_last_name):
        # Check doctor name is unique and not blank
        name = Doctor.query.filter_by(user_id=current_user.id, doctor_first_name=self.doctor_first_name.data, doctor_last_name=doctor_last_name.data).first()
        if name is not None:
            raise ValidationError("You already have a doctor with this name")
        if doctor_last_name.data.isspace() == True:
            raise ValidationError('Doctor names cannot be blank')

    def validate_doctor_state(self, doctor_state):
        # Ensure state is alphanumeric (this should be unnecessary due to changing
        # it to a select list)
        if doctor_state.data.isalpha() == False:
            raise ValidationError("Please select a state")
        
    def validate_doctor_zipcode(self, doctor_zipcode):
        # Check zipcode is 5 digits long (the form sets the max length, so we only
        # need a minimum)
        if len(doctor_zipcode.data) < 5:
            raise ValidationError("Zipcode must be a 5 digit number")
        try:
            zip = int(doctor_zipcode.data)
        except ValueError:
            raise ValidationError("Zipcode must be a 5 digit number") 
        

class EditDoctorForm(FlaskForm):
    """A form for editing doctor information"""
    doctor_first_name = StringField('First name (optional)', validators=[Length(max=64)])
    doctor_last_name = StringField('Last name', validators=[DataRequired(), Length(max=64)])
    doctor_phone_number = TelField('Telephone number', validators=[Optional(), Regexp(regex="^[0-9]{3}-[0-9]{3}-[0-9]{4}$", message="Valid format is xxx-xxx-xxxx")])
    doctor_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    doctor_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    doctor_city = StringField('City', validators=[Length(max=64)])
    doctor_state = SelectField('State', validators=[Optional()], choices=states)
    doctor_zipcode = StringField('Zipcode', validators=[Length(max=5), Optional()])
    doctor_notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')

    def __init__(self, original_full_name, *args, **kwargs):
        super(EditDoctorForm, self).__init__(*args, **kwargs)
        self.original_full_name = original_full_name

    def validate_doctor_last_name(self, doctor_last_name):
        # Check doctor name is unique and not blank
        if doctor_last_name.data.isspace() == True:
            raise ValidationError('Doctor names cannot be blank')
        if self.doctor_first_name.data:
            doctor_name = self.doctor_first_name.data + " " + doctor_last_name.data
        else:
            doctor_name = doctor_last_name.data

        if doctor_name != self.original_full_name:
            name = Doctor.query.filter_by(user_id=current_user.id, doctor_first_name=self.doctor_first_name.data, doctor_last_name=doctor_last_name.data).first()
            if name is not None:
                raise ValidationError("You already have a doctor with this name")
 
    def validate_doctor_state(self, doctor_state):
        # Ensure state is alphanumeric (this should be unnecessary due to changing
        # it to a select list)
        if doctor_state.data.isalpha() == False:
            raise ValidationError("Please select a state")
        
    def validate_doctor_zipcode(self, doctor_zipcode):
        # Check zipcode is 5 digits long (the form sets the max length, so we only
        # need a minimum)
        if len(doctor_zipcode.data) < 5:
            raise ValidationError("Zipcode must be a 5 digit number")
        try:
            zip = int(doctor_zipcode.data)
        except ValueError:
            raise ValidationError("Zipcode must be a 5 digit number")



class AddPharmacyForm(FlaskForm):
    """A form for adding a pharmacy"""
    pharmacy_name = StringField('Name of Pharmacy', validators=[Length(max=64), DataRequired()])
    pharmacy_phone_number = TelField('Telephone number', validators=[Optional(), Regexp(regex="^[0-9]{3}-[0-9]{3}-[0-9]{4}$", message="Valid format is xxx-xxx-xxxx")])
    pharmacy_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    pharmacy_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    pharmacy_city = StringField('City', validators=[Length(max=64)])
    pharmacy_state = SelectField('State', validators=[Optional()], choices=states)
    pharmacy_zipcode = StringField('Zipcode', validators=[Length(max=5), Optional()])
    pharmacy_notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')

    def validate_pharmacy_name(self, pharmacy_name):
        # Check pharmacy name is unique and not blank
        check_name = Pharmacy.query.filter_by(user_id=current_user.id, pharmacy_name=pharmacy_name.data).first()
        if check_name is not None:
            raise ValidationError("You already have a pharmacy with this name.")
        if pharmacy_name.data.isspace() == True:
            raise ValidationError("You cannot leave a blank name.")

    def validate_pharmacy_state(self, pharmacy_state):
        # Ensure state is alphanumeric (this should be unnecessary due to changing
        # it to a select list)
        if pharmacy_state.data.isalpha() == False:
            raise ValidationError("Please select a state")
        
    def validate_pharmacy_zipcode(self, pharmacy_zipcode):
        # Check zipcode is 5 digits long (the form sets the max length, so we only
        # need a minimum)
        if len(pharmacy_zipcode.data) < 5:
            raise ValidationError("Zipcode must be a 5 digit number")
        try:
            zip = int(pharmacy_zipcode.data)
        except ValueError:
            raise ValidationError("Zipcode must be a 5 digit number")

class EditPharmacyForm(FlaskForm):
    pharmacy_name = StringField('Name of Pharmacy', validators=[Length(max=64), DataRequired()])
    pharmacy_phone_number = TelField('Telephone number', validators=[Optional(), Regexp(regex="^[0-9]{3}-[0-9]{3}-[0-9]{4}$", message="Valid format is xxx-xxx-xxxx")])
    pharmacy_address_line_1 = StringField('Address line 1', validators=[Length(max=64)])
    pharmacy_address_line_2 = StringField('Address line 2', validators=[Length(max=64)])
    pharmacy_city = StringField('City', validators=[Length(max=64)])
    pharmacy_state = SelectField('State', validators=[Optional()], choices=states)
    pharmacy_zipcode = StringField('Zipcode', validators=[Length(max=5), Optional()])
    pharmacy_notes = TextAreaField('Notes', validators=[Length(max=128)])
    submit = SubmitField('Submit')

    def __init__(self, original_name, *args, **kwargs):
        super(EditPharmacyForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
 
    def validate_pharmacy_name(self, pharmacy_name):
        # Check pharmacy name is unique and not blank
        if pharmacy_name.data.isspace() == True:
            raise ValidationError("You cannot leave a blank name.")
        if pharmacy_name.data != self.original_name:
            check_name = Pharmacy.query.filter_by(user_id=current_user.id, pharmacy_name=pharmacy_name.data).first()
            if check_name is not None:
                raise ValidationError("You already have a pharmacy with this name.")

    def validate_pharmacy_state(self, pharmacy_state):
        # Ensure state is alphanumeric (this should be unnecessary due to changing
        # it to a select list)
        if pharmacy_state.data.isalpha() == False:
            raise ValidationError("Please select a state")
        
    def validate_pharmacy_zipcode(self, pharmacy_zipcode):
        # Check zipcode is 5 digits long (the form sets the max length, so we only
        # need a minimum)
        if len(pharmacy_zipcode.data) < 5:
            raise ValidationError("Zipcode must be a 5 digit number")
        try:
            zip = int(pharmacy_zipcode.data)
        except ValueError:
            raise ValidationError("Zipcode must be a 5 digit number")
        
class EmptyForm(FlaskForm):
    """Generic submit button"""
    submit = SubmitField('Submit')

class DeleteProfileForm(FlaskForm):
    """Multiply-confirmed delete profile form"""
    delete_confirmation = RadioField('Are you certain you wish to delete your account?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    extra_confirmation = RadioField('There is no undoing this action - are you completely certain?', choices=[('certain-no', 'No'), ('certain-yes', 'Yes')], default='certain-no')
    submit = SubmitField('Permanently delete this account')
    
class DeleteDoctorForm(FlaskForm):
    """Form to delete doctor (after confirmation)"""
    delete_confirmation = RadioField('Are you certain you wish to delete this doctor?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    submit = SubmitField('Permanently delete this doctor')

class DeleteMedicationForm(FlaskForm):
    """Form to delete medication (after confirmation)"""
    delete_confirmation = RadioField('Are you certain you wish to delete this medication?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    submit = SubmitField('Permanently delete this medication')    

class DeletePharmacyForm(FlaskForm):
    """Form to delete pharmacy (after confirmation)"""
    delete_confirmation = RadioField('Are you certain you wish to delete this pharmacy?', choices=[('delete-no', 'No'), ('delete-yes', 'Yes')], default='delete-no')
    submit = SubmitField('Permanently delete this pharmacy')