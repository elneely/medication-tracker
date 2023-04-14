from flask import render_template
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    meds = [
        {
            'medication_name': 'Naproxen',
            'brand_name': 'Aleve',
            'dose': '500 mg',
            'frequency': 'twice daily',
            'prescription_date': '01/01/2023',
            'last_filled': '04/03/2023',
            'short_term': 'n',
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
            'short_term': 'n',
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
            'short_term': 'n',
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
    return render_template('index.html', title='Home', meds=meds)

