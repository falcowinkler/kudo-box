from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length


class KudosForm(FlaskForm):
    sender = StringField('From', default="anonymous")
    receiver = StringField('To', default="anonymous")
    text = TextAreaField('Text', validators=[DataRequired(), Length(min=5, max=200)])
    token_tag = HiddenField("token")
    refresh_token_tag = HiddenField("refresh_token")
    token_expiration_tag = HiddenField("expiration")
    submit = SubmitField('Put in kudo box')
