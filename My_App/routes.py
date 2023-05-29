from flask import Blueprint
from forms import RegistrationForm
from flask import render_template

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
       return "success"
    return render_template('registration.html', form=form)



@app_routes.route('/index')
def index():
    return 'Index Page'

