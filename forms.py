from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Length,Email

class LoginForm(FlaskForm):
    name = StringField('NAME', validators=[DataRequired()])
    email = StringField('EMAIL', validators=[DataRequired(),Email(message="Enter Valid Email")])
    phone = StringField('PHONE',validators=[DataRequired(),Length(min=10,max=10,message="Enter a 10 digit Phone ")])
    submitapp = SubmitField('Take Appointment')
    submitchat = SubmitField('Take Remote Appointment(Chat)')