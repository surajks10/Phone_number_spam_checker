from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from models import db, bcrypt, jwt
from config import Config
from userModules.user import UserRegister, UserLogin, UserProfile
from userModules.contact import ContactList
from userModules.search import SearchByName, SearchByPhoneNumber
from userModules.search import ReportSpam

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

# Auth and User Endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserProfile, '/profile')

# Contact Management
api.add_resource(ContactList, '/contacts')

# Search and Spam Reporting
api.add_resource(SearchByName, '/search/name')
api.add_resource(SearchByPhoneNumber, '/search/phone')
api.add_resource(ReportSpam, '/report/spam')

if __name__ == '__main__':
    app.run(debug=True)
