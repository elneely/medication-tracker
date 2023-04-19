from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import User, Medication, Doctor, Pharmacy
from app.main.forms import MedicationForm, AddDoctorForm, EmptyForm
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
#    page = request.args.get('page', 1, type=int)
    meds = [
        {
            'medication_name': 'Naproxen',
            'brand_name': 'Aleve',
            'dose': '500 mg',
            'frequency': 'twice daily',
            'prescription_date': '01/01/2023',
            'last_filled': '04/03/2023',
            'short_term': False,
            'doctor': 'Dr. Smith',
            'pharmacy_name': 'CVS Caremark mail in',
            'pharmacy_info': '',
            'refills_remaining': '2',
            'refills_expiration': '01/01/2024',
            'length': '90 days',
            'reason': 'arthritis',
            'notes': 'I do better if I take this with food.',

        },

        {
            'medication_name': 'Cyclobenzaprine',
            'brand_name': 'Flexeril',
            'dose': '10 mg',
            'frequency': 'once at bedtime',
            'prescription_date': '03/03/2023',
            'last_filled': '04/01/2023',
            'short_term': False,
            'doctor': 'Dr. Jones',
            'pharmacy_name': 'Walgreens in Lenexa',
            'pharmacy_info': 'At the corner of Lackman and 87th Street',
            'refills_remaining': '4',
            'refills_expiration': '09/03/2023',
            'length': '30 days',
            'reason': 'muscle pain',
            'notes': '',
        },

          {
            'medication_name': 'Cephalexin',
            'brand_name': 'Keflex',
            'dose': '250 mg',
            'frequency': 'four times daily',
            'prescription_date': '04/11/2023',
            'last_filled': '04/11/2023',
            'short_term': True,
            'doctor': 'Dr. Smith',
            'pharmacy_name': 'Walgreens in Lenexa',
            'pharmacy_info': 'At the corner of Lackman and 87th Street',
            'refills_remaining': '0',
            'refills_expiration': '',
            'length': '10 days',
            'reason': 'Bronchitis',
            'notes': 'Smells bad',
        }
    ]
    form = EmptyForm()
    return render_template('user.html', title="Summary", user=user, meds=meds, form=form)

@bp.route('/user/<username>/user_profile')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user_profile.html', title="User Profile", user=user, form=form)


@bp.route('/user/<username>/add_medication', methods=['GET', 'POST'])
@login_required
def add_medication(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = MedicationForm()
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
        )
        db.session.add(medication)
        db.session.commit()
        flash(f'You have successfully added {form.medication_name.data} to your medication list.')
        return redirect(url_for('main.user', username=username))
    return render_template('add_medication.html', title='Add Medication', user=user, form=form)

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
    """
    doctors = [
        {"user_id" : current_user.id,
         "first_name" : "Jonathan",
         "last_name" : "Gendel",
         "phone_number" : "1234567890",
         "city" : "Munchtopia",
         "state": "",
         "zipcode" : "22066",
         "notes" : "Pillows!"
         },
        {"user_id" : current_user.id,
         "first_name" : "Rosie",
         "last_name" : "McDonaldson",
         "phone_number" : "1234567890",
         "address_line_1" : "Somewhere",
         "address_line_2" : "",
         "city" : "Munchtopia",
         "state": "",
         "zipcode" : "22066",
         "notes" : "Nose!"
         },
    ]
"""
    doctors = current_user.doctor_list().all()
    return render_template('doctor_list.html', title="Doctor List", user=user, doctors=doctors, form=form)

    