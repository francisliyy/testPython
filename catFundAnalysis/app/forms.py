from flask_wtf import Form
from wtforms import SelectField,SubmitField

class TOBForm(Form):
  type_of_building = SelectField(u'Type of Building', choices=[('pr_lr', 'Commercial'), ('pr_residential', 'Residential'), ('pr_mobile', 'Mobile Homes'), ('pr_rental','Tenants'), ('pr_condo','Condos')])
  submit = SubmitField('submit')