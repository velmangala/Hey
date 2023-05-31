from flask import Flask, abort
from routes import login
from routes import app_routes
from models import db, User
from utils import roles_required
from flask_login import LoginManager, UserMixin
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed


app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Hey.db'

login_manager = LoginManager()
principal = Principal(app)


@login_manager.user_loader
def load_user(user_id):
    # Implement code to load and return the user based on the user_id
    # This could involve querying your database or other user storage mechanism
    # Return the user object if found, or None if not found
    return User.query.get(user_id)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Customize the user identity object with roles or permissions as needed
    pass

login_manager.init_app(app)
login_manager.login_view = 'login'




# Import and register your routes here
app.register_blueprint(app_routes)

db.init_app(app)
if __name__ == '__main__':
    app.run(debug=True)
