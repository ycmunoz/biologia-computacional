from wtforms import Form
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, SelectField, FieldList

class protein_form(FlaskForm):
	specie_list = SelectField('Specie List')
	protein_list = SelectField('Protein List')

class gen_form(FlaskForm):
	specie_list = SelectField('Specie List')
	gen_list = SelectField('Gen List')

class tree_form(FlaskForm):
	specie_list = SelectField('Specie List')
	tree_list = SelectField('Tree List')