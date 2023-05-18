from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import User, Medication, Doctor, Pharmacy
from app.main.forms import AddDoctorForm, AddMedicationForm, AddPharmacyForm, EditDoctorForm, EditMedicationForm, EditPharmacyForm, EmptyForm
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    medications = current_user.medication_list().all()
    return render_template('user.html', title="Summary", user=user, medications=medications, form=form)

@bp.route('/user/<username>/user_profile')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    doctors = current_user.doctor_choices()
    return render_template('user_profile.html', title="User Profile", user=user, doctors=doctors, form=form)


@bp.route('/user/<username>/add_medication', methods=['GET', 'POST'])
@login_required
def add_medication(username):
    form = AddMedicationForm()
    form.doctor_list.choices = current_user.doctor_choices()
    form.pharmacy_list.choices = current_user.pharmacy_choices()
    
# if there's a new doctor, need to make the new doctor and submit it but then use
# that new id number for the doctor id
# if not, can just take it from form


    if form.validate_on_submit():
# Add new doctor to Doctor table
        last_data = form.new_doctor_last.data
        if last_data and (last_data.isspace() == False):
            new_doctor = Doctor(
            last_name=form.new_doctor_last.data,
            first_name=form.new_doctor_first.data,
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
                name=form.new_pharmacy_name.data,
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
            notes=form.notes.data,
            user_id=current_user.id,
            doctor_id=med_doctor_id,
            pharmacy_id=pharm_id
        )
        db.session.add(medication)
        db.session.commit()
        flash(f'You have successfully added {form.medication_name.data} to your medication list.')
        return redirect(url_for('main.user', username=username))
    return render_template('add_medication.html', title='Add Medication', user=user, form=form)


@bp.route('/user/<username>/medication/<medication_id>', methods=['GET', 'POST'])
@login_required
def medication(username, medication_id):
    user = User.query.filter_by(username=username).first_or_404()
    medication = Medication.query.filter_by(id=medication_id).first_or_404()
    form = EditMedicationForm(medication.medication_name, doctor_list=medication.doctor_id, pharmacy_list=medication.pharmacy_id)
    form.doctor_list.choices = current_user.doctor_choices()
    form.pharmacy_list.choices = current_user.pharmacy_choices()
    if form.validate_on_submit():
        # need to put in the if clause for if it's None for doctor/pharm
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
        medication.notes=form.notes.data
        medication.doctor_id=form.doctor_list.data,
        medication.pharmacy_id=form.pharmacy_list.data
        db.session.commit()
        flash(f'You have successfully edited information for {form.medication_name.data}.')
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
        form.notes.data=medication.notes
    return render_template('medication.html', title="Medication Information", user=user, medication=medication, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)



@bp.route('/user/<username>/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = AddDoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            address_line_1=form.address_line_1.data,
            address_line_2=form.address_line_2.data,
            city=form.city.data,
            state=form.state.data,
            zipcode=form.zipcode.data,
            notes=form.notes.data,
            user_id = current_user.id,
        )
        db.session.add(doctor)
        db.session.commit()
        flash(f'You have successfully added Dr. {form.last_name.data} to your doctor list.')
        return redirect(url_for('main.user', username=username))
    return render_template('add_doctor.html', title='Add Doctor', user=user, form=form)

@bp.route('/user/<username>/doctor_list', methods=['GET'])
@login_required
def doctor_list(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    doctors = current_user.doctor_list().all()
    return render_template('doctor_list.html', title="Doctor List", user=user, doctors=doctors, form=form)

@bp.route('/user/<username>/doctor/<doctor_id>', methods=['GET', 'POST'])
@login_required
def doctor(username, doctor_id):
    user = User.query.filter_by(username=username).first_or_404()
    doctor = Doctor.query.filter_by(id=doctor_id).first_or_404()
    doctor_name = doctor.full_name()
    form = EditDoctorForm(doctor_name)
    if form.validate_on_submit():
        doctor.first_name=form.first_name.data
        doctor.last_name=form.last_name.data
        doctor.phone_number=form.phone_number.data
        doctor.address_line_1=form.address_line_1.data
        doctor.address_line_2=form.address_line_2.data
        doctor.city=form.city.data
        doctor.state=form.state.data
        doctor.zipcode=form.zipcode.data
        doctor.notes=form.notes.data
        db.session.commit()
        flash(f'You have successfully edited information for Dr. {form.last_name.data}.')
    elif request.method == 'GET':
        form.first_name.data = doctor.first_name
        form.last_name.data = doctor.last_name
        form.phone_number.data = doctor.phone_number
        form.address_line_1.data = doctor.address_line_1
        form.address_line_2.data = doctor.address_line_2
        form.city.data = doctor.city
        form.state.data = doctor.state
        form.zipcode.data = doctor.zipcode
        form.notes.data = doctor.notes
    return render_template('doctor.html', title="Doctor Information", user=user, doctor=doctor, form=form)

@bp.route('/user/<username>/add_pharmacy', methods=['GET', 'POST'])
@login_required
def add_pharmacy(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = AddPharmacyForm()
    if form.validate_on_submit():
        pharmacy = Pharmacy(
            name=form.name.data,
            phone_number=form.phone_number.data,
            address_line_1=form.address_line_1.data,
            address_line_2=form.address_line_2.data,
            city=form.city.data,
            state=form.state.data,
            zipcode=form.zipcode.data,
            notes=form.notes.data,
            user_id = current_user.id,
        )
        db.session.add(pharmacy)
        db.session.commit()
        flash(f'You have successfully added {form.name.data} to your pharmacy list.')
        return redirect(url_for('main.user', username=username))
    return render_template('add_pharmacy.html', title='Add Pharmacy', user=user, form=form)

@bp.route('/user/<username>/pharmacy_list', methods=['GET'])
@login_required
def pharmacy_list(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    pharmacies = current_user.pharmacy_list().all()
    return render_template('pharmacy_list.html', title="Pharmacy List", user=user, pharmacies=pharmacies, form=form)


@bp.route('/user/<username>/pharmacy/<pharmacy_id>', methods=['GET', 'POST'])
@login_required
def pharmacy(username, pharmacy_id):
    user = User.query.filter_by(username=username).first_or_404()
    pharmacy = Pharmacy.query.filter_by(id=pharmacy_id).first_or_404()
    form = EditPharmacyForm(pharmacy.name)
    if form.validate_on_submit():
        pharmacy.name=form.name.data
        pharmacy.phone_number=form.phone_number.data
        pharmacy.address_line_1=form.address_line_1.data
        pharmacy.address_line_2=form.address_line_2.data
        pharmacy.city=form.city.data
        pharmacy.state=form.state.data
        pharmacy.zipcode=form.zipcode.data
        pharmacy.notes=form.notes.data
        db.session.commit()
        flash(f'You have successfully edited information for {form.name.data}.')
    elif request.method == 'GET':
        form.name.data = pharmacy.name
        form.phone_number.data = pharmacy.phone_number
        form.address_line_1.data = pharmacy.address_line_1
        form.address_line_2.data = pharmacy.address_line_2
        form.city.data = pharmacy.city
        form.state.data = pharmacy.state
        form.zipcode.data = pharmacy.zipcode
        form.notes.data = pharmacy.notes
    return render_template('pharmacy.html', title="Pharmacy Information", user=user, pharmacy=pharmacy, form=form)

