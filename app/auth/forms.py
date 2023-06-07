from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    display_name = StringField('Display name (optional)')
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', 
            message="Passwords must match.")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different username')
        elif username.data.isspace() == True:
            raise ValidationError('Usernames cannot be blank')
        elif username.data.isalnum() == False:
            raise ValidationError('Usernames can only contain letters and numbers')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
    
    def validate_password(self, password):
        if password.data.isspace() == True:
            raise ValidationError('Passwords cannot be blank')
        elif len(password.data) < 8:
            raise ValidationError('Passwords must be at least 8 characters')
        elif len(password.data.split()) > 1:
            raise ValidationError('Passwords cannot contain a space')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Submit')

    def validate_new_password(self, new_password):
        if new_password.data.isspace() == True:
            raise ValidationError('Passwords cannot be blank')
        elif len(new_password.data) < 8:
            raise ValidationError('Passwords must be at least 8 characters')
        elif len(new_password.data.split()) > 1:
            raise ValidationError('Passwords cannot contain a space')