from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.models import User
from app.auth.forms import ChangePasswordForm, LoginForm, RegistrationForm, \
    ResetPasswordForm, ResetPasswordRequestForm
from app.auth.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Log a user in
    if current_user.is_authenticated:
        return redirect(url_for('main.user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = url_for('main.user', username=current_user.username)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)     
    return render_template('auth/login.html', title="Sign In", form=form)

@bp.route('/logout')
def logout():
    # Log a user out
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Register a new user
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), 
                    display_name=form.display_name.data, 
                    email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/<username>/change_password', methods=['GET', 'POST'])
@login_required
def change_password(username):
    # Allows a user to change their password
    user = User.query.filter_by(username=username).first_or_404()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not user.check_password(form.current_password.data):
            flash('Invalid password')
            return redirect(url_for('auth.change_password', username=username))
        else:
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been changed')
            return redirect(url_for('main.user_profile', username=username))
    return render_template('auth/change_password.html', title="Change Password", user=user, form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # Sends a password reset email to the user
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Allows user to reset their password via the email token
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
