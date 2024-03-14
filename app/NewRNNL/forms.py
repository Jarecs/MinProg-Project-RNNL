from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, Optional


class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[Optional()])
    event_location = StringField('Event Location', validators=[InputRequired(), Length(1, 64)])
    event_date = DateField('Event Date', validators=[InputRequired()])
    event_time = TimeField('Event Time', validators=[InputRequired()])
    event_description = StringField('Event Description', validators=[Optional(), Length(1, 64)])
    event_is_private = BooleanField('Private Event')
    event_password = PasswordField('Event Password', validators=[Optional(), Length(1, 128)])
    submit = SubmitField('Submit')
