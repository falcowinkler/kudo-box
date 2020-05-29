from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class KudosForm(FlaskForm):
    sender = StringField('From')
    receiver = StringField('To')
    text = TextAreaField('Text', validators=[DataRequired()])
    token_tag = HiddenField("token")
    refresh_token_tag = HiddenField("refresh_token")
    token_expiration_tag = HiddenField("expiration")
    submit = SubmitField('Put in kudo box')
