from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import SupportGroup



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    age = IntegerField('Age', validators=[DataRequired()])
    # Add more fields as needed

    submit = SubmitField('Submit')

class SupportGroupForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    # Add more fields as needed for your SupportGroup model

    # You can also add custom validators for specific fields if needed
    def validate_title(self, field):
        # Implement custom validation logic, such as checking for unique titles
        # Example: Check if the title already exists in the database
        existing_group = SupportGroup.query.filter_by(title=field.data).first()
        if existing_group:
            raise ValidationError('This title is already taken. Please choose a different one.')
        

class ForumPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[
                            DataRequired(), Length(max=500)])
