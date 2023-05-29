from flask import Flask
from routes import app_routes
from models import db

app = Flask(__name__)

app.register_blueprint(app_routes)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Hey.db'



db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
