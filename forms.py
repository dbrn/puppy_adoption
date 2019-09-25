from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class AddPup(FlaskForm):
    pup_name = StringField("Pup's name: ", [DataRequired()])
    submit = SubmitField("Send")


class DeletePup(FlaskForm):
    pup_id = StringField("Pup's ID: ", [DataRequired(), NumberRange()])
    submit = SubmitField("Send")


class AddOwner(FlaskForm):
    owner_name = StringField("Owner's name: ", [DataRequired()])
    pup_id = StringField("Pup's id: ", [DataRequired(), NumberRange()])
    submit = SubmitField("Send")
