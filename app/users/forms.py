
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from app.models import User
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     )
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=6, max=10)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    '''def validate_field(self, field):

        if True:
            raise ValidationError('Validation Message')'''

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username is already taken')

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('Email is already taken')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remeber Me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=6, max=10)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Profile', validators=[
        FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    '''def validate_field(self, field):

        if True:
            raise ValidationError('Validation Message')'''

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email is already taken')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])

    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), EqualTo('new_password')])

    submit = SubmitField('Request Password Reset')
