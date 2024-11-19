from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

import secrets


app = Flask(__name__, template_folder='templates')
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)

# Flask-WTF requires this line
csrf = CSRFProtect(app)

class SLAPolicyForm(FlaskForm):
    name = StringField('SLA policy name', validators=[DataRequired(), Length(10, 40)])
    description = StringField('Description (Optional)')
    warehouse_ids = StringField('Warehouse IDs (comma-separated)', validators=[DataRequired(), Length(10, 40)])
    sla_mode = SelectField('Policy mode', choices=[('All', 'ALL'), ('SLA Burst', 'SLA_BURST'), ('Error', 'ERROR')])
    sla_seconds = StringField('SLA in seconds', validators=[DataRequired(), Length(10, 40)])
    included_statuses = SelectMultipleField(choices=[('1', 'QUEUED'), ('2', 'RUNNING'), ('3', 'FAILED'), ('4', 'FINISHED')], default = ['1','2','3','4','5'])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET'])
def index():
    names = []

    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = SLAPolicyForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name.lower() in names:
            # empty the form field
            form.name.data = ""
            id = '1234567890'
            # redirect the browser to another route and template
            return redirect( url_for('actor', id=id) )
        else:
            message = "That actor is not in our database."

    return render_template('index.html', names=names, form=form, message=message)
