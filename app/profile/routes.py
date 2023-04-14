from flask import render_template
from app.profile.forms import EmptyForm
from app.profile import bp

@bp.route('/user_profile')
def user_profile():
    form = EmptyForm()
    return render_template('profile/user_profile.html', title="User Profile", form=form)