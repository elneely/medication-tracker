from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import User, Medication, Doctor, Pharmacy
from app.main.forms import MedicationForm, AddDoctorForm, AddPharmacyForm, EmptyForm
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
    meds = current_user.medication_list().all()
    return render_template('user.html', title="Summary", user=user, meds=meds, form=form)

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
    user = User.query.filter_by(username=username).first_or_404()
    doctors = current_user.doctor_choices()
    form = MedicationForm()
    # succeeds at populating the form with doctors but I don't seem to have the data coming back in the
    # right format.  Not sure if it's because I wrote the html by hand for this and flask form won't
    # play nicely or if there's something else going on.
    
    if form.validate_on_submit():
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
            doctor_id=int(form.doctor_id.data)
        )
        db.session.add(medication)
        db.session.commit()
        flash(f'You have successfully added {form.medication_name.data} to your medication list.')
        return redirect(url_for('main.user', username=username))
    return render_template('add_medication.html', title='Add Medication', doctors=doctors, user=user, form=form)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacy.id'))
  
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
