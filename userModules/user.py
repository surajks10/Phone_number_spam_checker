from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db

# Registration
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('phone_number', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('email', type=str, required=False)

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return {"message": "User with this phone number already exists."}, 400

        user = User(name=data['name'], phone_number=data['phone_number'], email=data.get('email'))
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully."}, 201

# Login
class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        data = UserLogin.parser.parse_args()
        user = User.query.filter_by(phone_number=data['phone_number']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials."}, 401

# Profile
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return {
                "name": user.name,
                "phone_number": user.phone_number,
                "email": user.email
            }, 200
        return {"message": "User not found."}, 404
