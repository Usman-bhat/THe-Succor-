from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskapp.dbmodels import Users
from flask_login import current_user


class Regestrationform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=10)])
    email = StringField('Email', validators=[DataRequired()])
    ph_no = StringField('phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confpass = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Taken Please Take different one')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Taken Please Take different one')


class Loginform(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login in')

class Contactform(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ph_no = StringField('Phone number', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class updateform(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    about_me = StringField('about me')
    ph_no = StringField('Phone no.', validators=[DataRequired()])
    img_file = FileField('Profile picture', validators=[FileAllowed(['jpeg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Taken Please Take different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Taken Please Take different one')



class Postform(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('slug', validators=[DataRequired(), Length(min=5, max=10), ])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('submit')


class Edit_post_form(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('submit')

