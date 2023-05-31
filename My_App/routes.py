from crypt import methods
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import *
from models import *
from utils import *




app_routes = Blueprint('app_routes', __name__)
api_routes = Blueprint('api_routes', __name__)

api_routes.route('/api/register', methods=['POST'])
@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app_routes.route('/api/login', methods=['POST'])
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
@api_routes.route('/api/logout')
@app_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('app_route.index'))

@api_routes.route('/api/index')
@app_routes.route('/index')
def index():
    return 'Index Page'

@api_routes.route('/api/profile', methods=['GET', 'POST'])
@app_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@api_routes.route('/api/edit_profile', methods=['GET', 'POST'])
@app_routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    data = request.get_json()
    # Retrieve the necessary data from the request JSON
    name = data.get('name')
    email = data.get('email')

    # Update the user's profile information
    current_user.name = name
    current_user.email = email

    # Save the changes to the database
    db.session.commit()

    # Return a JSON response indicating success
    return jsonify({'message': 'Profile updated successfully'})


@api_routes.route('/api/complete_profile', methods=['GET', 'POST'])
@app_routes.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Update the user's profile information in the database
        current_user.name = form.name.data
        current_user.age = form.age.data
        # Add more fields as needed
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    return render_template('complete_profile.html', form=form)

@api_routes.route('/api/dashboard')
@app_routes.route('/dashboard')
@login_required  # Use the @login_required decorator to protect the route
def dashboard():
    # Route accessible only for authenticated users
    pass


@api_routes.route('/api/admin', methods=['GET', 'POST'])
@app_routes.route('/admin')
# Use the @roles_required decorator to check for specific roles
@roles_required('admin')
def admin_panel():
    # Route accessible only for users with 'admin' role
    pass
