from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import *
from models import *




app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
       return "success"
    return render_template('registration.html', form=form)


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "success"

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


# Logout route
@app_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('app_route.index'))

@app_routes.route('/index')
def index():
    return 'Index Page'

