from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import User, Medication, Doctor, Pharmacy
from app.main.forms import AddDoctorForm, AddMedicationForm, AddPharmacyForm, \
    DeleteDoctorForm, DeleteMedicationForm, DeletePharmacyForm, \
    DeleteProfileForm, EditDoctorForm, EditMedicationForm, EditPharmacyForm, \
    EditProfileForm, EmptyForm, ManageMedicationsForm
from app.main import bp

# Home page for unauthenticated users and redirect for authenticated users
@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.user', username=current_user.username))
    return render_template('index.html', title='Home')

# Help page
@bp.route('/help')
def help():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        return render_template('help.html', title="Help page", user=user)
    return render_template('help.html', title="Help page")

# Home page for authenticated users
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    medications = current_user.medication_list().all()
    reminders = current_user.refill_list()
    return render_template('user.html', title="Summary", 
                           user=user, medications=medications, form=form, reminders=reminders)

# User profile page
@bp.route('/user/<username>/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = DeleteProfileForm()
    reminders = current_user.refill_list()
    if form.validate_on_submit():
        if form.delete_confirmation.data == 'delete-yes' and form.extra_confirmation.data == 'certain-yes':
            """
            I think this is all done with the cascade - check this
            medications = current_user.medication_list.all()
            doctors = current_user.doctor_list.all()
            pharmacies = current_user.doctor_list.all()
            for medication in medications:
                db.session.delete(medication)
            """
            db.session.delete(user)
            db.session.commit()
           
            flash('Your account has been deleted')
            return redirect(url_for('main.index'))
        elif form.delete_confirmation.data == 'delete-no' or form.extra_confirmation.data == 'certain-no':
            flash('If you want to delete your account, you must confirm twice.')
    return render_template('user_profile.html', title="User Profile", 
                           user=user, form=form, reminders=reminders)

# Edit profile page (to make changes to user info)
@bp.route('/user/<username>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm(username, user.email)
    if form.validate_on_submit():
        if (user.display_name == form.display_name.data and 
                user.email == form.email.data.lower() and 
                user.username == form.username.data.lower()):
            flash('You have made no changes')
            return redirect(url_for('main.user_profile', username=username))
        else:
            user.display_name = form.display_name.data
            user.email = form.email.data.lower()
            user.username = form.username.data.lower()
            db.session.commit()
            new_name = user.username
            flash('Your changes have been saved')
            return redirect(url_for('main.user_profile', username=new_name))
# Pre-fill the page with user info
    elif request.method == 'GET':
        form.username.data = user.username
        form.display_name.data = user.display_name
        form.email.data = user.email
    
    return render_template('edit_profile.html', title="Edit Profile", 
                           user=user, form=form)

# Manage medications page
@bp.route('/user/<username>/manage_medications', methods=['GET', 'POST'])
@login_required
def manage_medications(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ManageMedicationsForm()
    form.doctor_list.choices = current_user.doctor_choices()
    form.pharmacy_list.choices = current_user.pharmacy_choices()
    form.selected_medications.choices = current_user.medication_choices()
    medications = current_user.medication_list().all()
    if form.validate_on_submit():
        selected_medications = form.selected_medications.data
# for each if clause
# for each selected medication, pull the medication with that id number
# perform appropriate modification
        if selected_medications == []:
            flash('You have not selected any medications')
        elif form.action_choice.data == 'default':
            flash('No action has been selected.')
        elif form.action_choice.data == 'change-doctor':
            for medication in selected_medications:
                med_id = int(medication)
                med = Medication.query.filter_by(id=med_id).first_or_404()
                med.doctor_id = form.doctor_list.data
            db.session.commit()
            flash('Medications updated.')
        elif form.action_choice.data == 'change-pharmacy':
            for medication in selected_medications:
                med_id = int(medication)
                med = Medication.query.filter_by(id=med_id).first_or_404()
                med.pharmacy_id = form.pharmacy_list.data
            db.session.commit()
            flash('Medications updated.')
        elif form.action_choice.data == 'delete-medication':
            if form.delete_confirmation.data == 'delete-yes':
                for medication in selected_medications:
                    med_id = int(medication)
                    med = Medication.query.filter_by(id=med_id).first_or_404()
                    db.session.delete(med)
                db.session.commit()
                flash('Medication list updated.')
            else:
                flash('You must confirm deletion of these medications')
        return redirect(url_for('main.manage_medications', username=username))  

    return render_template('manage_medications.html', title="Manage Medications", user=user, medications=medications, form=form)

# Add medication page
@bp.route('/user/<username>/add_medication', methods=['GET', 'POST'])
@login_required
def add_medication(username):
    form = AddMedicationForm()
    form.doctor_list.choices = current_user.doctor_choices()
    form.pharmacy_list.choices = current_user.pharmacy_choices()
    
# if there's a new doctor, need to make the new doctor and submit it in order 
# to use that new id number for the doctor id
# if not, can just take it from form

    if form.validate_on_submit():
# Add new doctor to Doctor table
        last_data = form.new_doctor_last.data
        if last_data and (last_data.isspace() == False):
            new_doctor = Doctor(
            doctor_last_name=form.new_doctor_last.data,
            doctor_first_name=form.new_doctor_first.data,
            user_id=current_user.id
            )
            db.session.add(new_doctor)
            db.session.flush()
            flash(f'You have successfully added Dr. {form.new_doctor_last.data} to your doctor list.')
# retrieve id of that new doctor
            med_doctor_id = new_doctor.id
        elif form.doctor_list.data:
            med_doctor_id=form.doctor_list.data
        else:
            med_doctor_id = None
        pharm_data = form.new_pharmacy_name.data
        if pharm_data and pharm_data.isspace() == False:
            new_pharmacy = Pharmacy(
                pharmacy_name=form.new_pharmacy_name.data,
                user_id=current_user.id
            )
            db.session.add(new_pharmacy)
            db.session.flush()
            flash(f'You have successfully added {form.new_pharmacy_name.data} to your pharmacy list.')
            pharm_id = new_pharmacy.id
        elif form.pharmacy_list.data:
            pharm_id = form.pharmacy_list.data
        else:
            pharm_id = None    
        medication = Medication(
            medication_name=form.medication_name.data,
            brand_name=form.brand_name.data,
            dose=form.dose.data,
            frequency=form.frequency.data,
            prescription_date=form.prescription_date.data,
            last_filled=form.last_filled.data,
            short_term=form.short_term.data,
            reminder=form.reminder.data,
            reminder_length=form.reminder_length.data,
            refills_remaining=form.refills_remaining.data,
            refills_expiration=form.refills_expiration.data,
            length=form.length.data,
            reason=form.reason.data,
            medication_notes=form.medication_notes.data,
            user_id=current_user.id,
            doctor_id=med_doctor_id,
            pharmacy_id=pharm_id
        )
        db.session.add(medication)
        db.session.commit()
        flash(f'You have successfully added {form.medication_name.data} to your medication list.')
        return redirect(url_for('main.user', username=username))
    return render_template('add_medication.html', title='Add Medication', user=user, form=form)

# Detailed info page for a specific medication
@bp.route('/user/<username>/medication/<medication_id>', methods=['GET', 'POST'])
@login_required
def medication(username, medication_id):
    user = User.query.filter_by(username=username).first_or_404()
    medication = Medication.query.filter_by(id=medication_id).first_or_404()
    name = medication.medication_name
    form=DeleteMedicationForm()
    if form.validate_on_submit():
        if form.delete_confirmation.data == 'delete-yes':
                db.session.delete(medication)
                db.session.commit()
                flash(f'{name} has been deleted')           
        return redirect(url_for('main.manage_medications', username=username))
    return render_template('medication.html', title="Medication Information", user=user, medication=medication, form=form)

# Edit medication page
@bp.route('/user/<username>/medication/<medication_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_medication(username, medication_id):
    user = User.query.filter_by(username=username).first_or_404()
    medication = Medication.query.filter_by(id=medication_id).first_or_404()
    if (medication.doctor_id != None) and (medication.pharmacy_id != None):
        form = EditMedicationForm(medication.medication_name, doctor_list=medication.doctor_id, pharmacy_list=medication.pharmacy_id)
    elif medication.doctor_id != None:
        form = EditMedicationForm(medication.medication_name, doctor_list=medication.doctor_id)
    elif medication.pharmacy_id != None:
        form = EditMedicationForm(medication.medication_name, pharmacy_list=medication.pharmacy_id)
    else:
        form = EditMedicationForm(medication.medication_name)
    form.doctor_list.choices = current_user.doctor_choices()
    form.pharmacy_list.choices = current_user.pharmacy_choices()
    if form.validate_on_submit():
        medication.medication_name=form.medication_name.data
        medication.brand_name=form.brand_name.data
        medication.dose=form.dose.data
        medication.frequency=form.frequency.data
        medication.prescription_date=form.prescription_date.data
        medication.last_filled=form.last_filled.data
        medication.short_term=form.short_term.data
        medication.reminder=form.reminder.data
        medication.reminder_length=form.reminder_length.data
        medication.refills_remaining=form.refills_remaining.data
        medication.refills_expiration=form.refills_expiration.data
        medication.length=form.length.data
        medication.reason=form.reason.data
        medication.medication_notes=form.medication_notes.data
        medication.doctor_id=form.doctor_list.data
        medication.pharmacy_id=form.pharmacy_list.data
        db.session.commit()
        flash(f'Any changes you have made to {form.medication_name.data} have been saved')
        return redirect(url_for('main.medication', username=username, medication=medication, medication_id=medication.id))
# Pre-fill the form with info for the medication
    elif request.method == 'GET':
        form.medication_name.data = medication.medication_name
        form.brand_name.data = medication.brand_name
        form.dose.data = medication.dose
        form.frequency.data = medication.frequency
        form.prescription_date.data = medication.prescription_date
        form.last_filled.data=medication.last_filled
        form.short_term.data=medication.short_term
        form.reminder.data=medication.reminder
        form.reminder_length.data=medication.reminder_length
        form.refills_remaining.data=medication.refills_remaining
        form.refills_expiration.data=medication.refills_expiration
        form.length.data=medication.length
        form.reason.data=medication.reason
        form.medication_notes.data=medication.medication_notes
    return render_template('edit_medication.html', title="Edit Medication", user=user, medication=medication, form=form)

# Add doctor page
@bp.route('/user/<username>/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = AddDoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            doctor_first_name=form.doctor_first_name.data,
            doctor_last_name=form.doctor_last_name.data,
            doctor_phone_number=form.doctor_phone_number.data,
            doctor_address_line_1=form.doctor_address_line_1.data,
            doctor_address_line_2=form.doctor_address_line_2.data,
            doctor_city=form.doctor_city.data,
            doctor_state=form.doctor_state.data,
            doctor_zipcode=form.doctor_zipcode.data,
            doctor_notes=form.doctor_notes.data,
            user_id = current_user.id,
        )
        db.session.add(doctor)
        db.session.commit()
        flash(f'You have successfully added Dr. {form.doctor_last_name.data} to your doctor list.')
        return redirect(url_for('main.doctor_list', username=username))
    return render_template('add_doctor.html', title='Add Doctor', user=user, form=form)

# Contact list for doctors 
@bp.route('/user/<username>/doctor_list', methods=['GET'])
@login_required
def doctor_list(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    doctors = current_user.doctor_list().all()
    return render_template('doctor_list.html', title="Doctor List", user=user, doctors=doctors, form=form)

# Detailed info for a specific doctor
@bp.route('/user/<username>/doctor/<doctor_id>', methods=['GET', 'POST'])
@login_required
def doctor(username, doctor_id):
    user = User.query.filter_by(username=username).first_or_404()
    doctor = Doctor.query.filter_by(id=doctor_id).first_or_404()
    name = doctor.doctor_last_name
    prescribed_medications = []
    medications = current_user.medication_list().all()
    for medication in medications:
        if medication.doctor_id == doctor.id:
            prescribed_medications.append(medication)
    form = DeleteDoctorForm()
    if form.validate_on_submit():
        if form.delete_confirmation.data == "delete-yes":
            medications = current_user.medication_list().all()
            for medication in medications:
                if medication.doctor_id == doctor.id:
                    medication.doctor_id = None 
            db.session.delete(doctor)
            db.session.commit()
            flash(f'Dr. {name} has been deleted')
            return redirect(url_for('main.doctor_list', username=username))
    return render_template('doctor.html', title="Doctor Information", user=user, doctor=doctor, form=form, medications=prescribed_medications)

# Edit doctor page
@bp.route('/user/<username>/doctor/<doctor_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_doctor(username, doctor_id):
    user = User.query.filter_by(username=username).first_or_404()
    doctor = Doctor.query.filter_by(id=doctor_id).first_or_404()
    doctor_name = doctor.full_name()
    form = EditDoctorForm(doctor_name)
    if form.validate_on_submit():
        if (doctor.doctor_first_name == form.doctor_first_name.data and
                doctor.doctor_last_name == form.doctor_last_name.data and
                doctor.doctor_phone_number == form.doctor_phone_number.data and
                doctor.doctor_address_line_1 == form.doctor_address_line_1.data and
                doctor.doctor_address_line_2 == form.doctor_address_line_2.data and
                doctor.doctor_city == form.doctor_city.data and
                doctor.doctor_state == form.doctor_state.data and
                doctor.doctor_zipcode == form.doctor_zipcode.data and
                doctor.doctor_notes == form.doctor_notes.data):
            flash(f'You have made no changes to Dr. {form.doctor_last_name.data}.')
            return redirect(url_for('main.doctor', username=username, doctor_id=doctor.id))
        else:   
            doctor.doctor_first_name=form.doctor_first_name.data
            doctor.doctor_last_name=form.doctor_last_name.data
            doctor.doctor_phone_number=form.doctor_phone_number.data
            doctor.doctor_address_line_1=form.doctor_address_line_1.data
            doctor.doctor_address_line_2=form.doctor_address_line_2.data
            doctor.doctor_city=form.doctor_city.data
            doctor.doctor_state=form.doctor_state.data
            doctor.doctor_zipcode=form.doctor_zipcode.data
            doctor.doctor_notes=form.doctor_notes.data
            db.session.commit()
            flash(f'You have successfully edited information for Dr. {form.doctor_last_name.data}.')
            return redirect(url_for('main.doctor', username=username, doctor_id=doctor.id))
# Pre-fill the form with info
    elif request.method == 'GET':
        form.doctor_first_name.data = doctor.doctor_first_name
        form.doctor_last_name.data = doctor.doctor_last_name
        form.doctor_phone_number.data = doctor.doctor_phone_number
        form.doctor_address_line_1.data = doctor.doctor_address_line_1
        form.doctor_address_line_2.data = doctor.doctor_address_line_2
        form.doctor_city.data = doctor.doctor_city
        form.doctor_state.data = doctor.doctor_state
        form.doctor_zipcode.data = doctor.doctor_zipcode
        form.doctor_notes.data = doctor.doctor_notes
    return render_template('edit_doctor.html', title="Doctor Information", user=user, doctor=doctor, form=form)

# Add pharmacy page
@bp.route('/user/<username>/add_pharmacy', methods=['GET', 'POST'])
@login_required
def add_pharmacy(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = AddPharmacyForm()
    if form.validate_on_submit():
        pharmacy = Pharmacy(
            pharmacy_name=form.pharmacy_name.data,
            pharmacy_phone_number=form.pharmacy_phone_number.data,
            pharmacy_address_line_1=form.pharmacy_address_line_1.data,
            pharmacy_address_line_2=form.pharmacy_address_line_2.data,
            pharmacy_city=form.pharmacy_city.data,
            pharmacy_state=form.pharmacy_state.data,
            pharmacy_zipcode=form.pharmacy_zipcode.data,
            pharmacy_notes=form.pharmacy_notes.data,
            user_id = current_user.id,
        )
        db.session.add(pharmacy)
        db.session.commit()
        flash(f'You have successfully added {form.pharmacy_name.data} to your pharmacy list.')
        return redirect(url_for('main.pharmacy_list', username=username))
    return render_template('add_pharmacy.html', title='Add Pharmacy', user=user, form=form)

# Pharmacy contact list
@bp.route('/user/<username>/pharmacy_list', methods=['GET'])
@login_required
def pharmacy_list(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    pharmacies = current_user.pharmacy_list().all()
    return render_template('pharmacy_list.html', title="Pharmacy List", user=user, pharmacies=pharmacies, form=form)

# Detailed info for a specific pharmacy
@bp.route('/user/<username>/pharmacy/<pharmacy_id>', methods=['GET', 'POST'])
@login_required
def pharmacy(username, pharmacy_id):
    user = User.query.filter_by(username=username).first_or_404()
    pharmacy = Pharmacy.query.filter_by(id=pharmacy_id).first_or_404()
    name = pharmacy.pharmacy_name
    prescribed_medications = []
    medications = current_user.medication_list().all()
    for medication in medications:
        if medication.pharmacy_id == pharmacy.id:
            prescribed_medications.append(medication)
    form = DeletePharmacyForm()
    if form.validate_on_submit():
        if form.delete_confirmation.data == "delete-yes":
            medications = current_user.medication_list().all()
            for medication in medications:
                if medication.pharmacy_id == pharmacy.id:
                    medication.pharmacy_id = None 
            db.session.delete(pharmacy)
            db.session.commit()
            flash(f'{name} has been deleted')
            return redirect(url_for('main.pharmacy_list', username=username))
    return render_template('pharmacy.html', title="Pharmacy Information", user=user, pharmacy=pharmacy, form=form, medications=prescribed_medications)

# Edit pharmacy page
@bp.route('/user/<username>/pharmacy/<pharmacy_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_pharmacy(username, pharmacy_id):
    user = User.query.filter_by(username=username).first_or_404()
    pharmacy = Pharmacy.query.filter_by(id=pharmacy_id).first_or_404()
    form = EditPharmacyForm(pharmacy.pharmacy_name)
    if form.validate_on_submit():
        if (pharmacy.pharmacy_name == form.pharmacy_name.data and
                pharmacy.pharmacy_phone_number == form.pharmacy_phone_number.data and
                pharmacy.pharmacy_address_line_1 == form.pharmacy_address_line_1.data and
                pharmacy.pharmacy_address_line_2 == form.pharmacy_address_line_2.data and
                pharmacy.pharmacy_city == form.pharmacy_city.data and
                pharmacy.pharmacy_state == form.pharmacy_state.data and
                pharmacy.pharmacy_zipcode == form.pharmacy_zipcode.data and
                pharmacy.pharmacy_notes == form.pharmacy_notes.data):
            flash(f'You have made no changes to {form.pharmacy_name.data}')
            return redirect(url_for('main.pharmacy', username=username, pharmacy_id=pharmacy.id))
        else:
            pharmacy.pharmacy_name=form.pharmacy_name.data
            pharmacy.pharmacy_phone_number=form.pharmacy_phone_number.data
            pharmacy.pharmacy_address_line_1=form.pharmacy_address_line_1.data
            pharmacy.pharmacy_address_line_2=form.pharmacy_address_line_2.data
            pharmacy.pharmacy_city=form.pharmacy_city.data
            pharmacy.pharmacy_state=form.pharmacy_state.data
            pharmacy.pharmacy_zipcode=form.pharmacy_zipcode.data
            pharmacy.pharmacy_notes=form.pharmacy_notes.data
            db.session.commit()
            flash(f'You have successfully edited information for {form.pharmacy_name.data}')
            return redirect(url_for('main.pharmacy', username=username, pharmacy_id=pharmacy.id))
# Pre-fill form with info 
    elif request.method == 'GET':
        form.pharmacy_name.data = pharmacy.pharmacy_name
        form.pharmacy_phone_number.data = pharmacy.pharmacy_phone_number
        form.pharmacy_address_line_1.data = pharmacy.pharmacy_address_line_1
        form.pharmacy_address_line_2.data = pharmacy.pharmacy_address_line_2
        form.pharmacy_city.data = pharmacy.pharmacy_city
        form.pharmacy_state.data = pharmacy.pharmacy_state
        form.pharmacy_zipcode.data = pharmacy.pharmacy_zipcode
        form.pharmacy_notes.data = pharmacy.pharmacy_notes
    return render_template('edit_pharmacy.html', title="Pharmacy Information", user=user, pharmacy=pharmacy, form=form)

