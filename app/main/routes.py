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
    form = MedicationForm()
    form.doctor_list.choices = current_user.doctor_choices()
    
# if there's a new doctor, need to make the new doctor and submit it but then use
# that new id number for the doctor id
# if not, can just take it from form


    if form.validate_on_submit():
# Add new doctor to Doctor table
        if form.new_doctor_last.data:
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
        else:
            med_doctor_id=form.doctor_list.data
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
            doctor_id=med_doctor_id
        )
        db.session.add(medication)
        db.session.commit()
        flash(f'You have successfully added {form.medication_name.data} to your medication list.')
        return redirect(url_for('main.user', username=username))
    return render_template('add_medication.html', title='Add Medication', user=user, form=form)


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
