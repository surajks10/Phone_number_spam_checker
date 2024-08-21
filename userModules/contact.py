from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Contact, db

# Manage Contacts
class ContactList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('phone_number', type=str, required=True)

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        contacts = Contact.query.filter_by(user_id=user_id).all()
        return [{"name": contact.name, "phone_number": contact.phone_number, "is_spam": contact.is_spam} for contact in contacts], 200

    @jwt_required()
    def post(self):
        data = ContactList.parser.parse_args()
        user_id = get_jwt_identity()
        contact = Contact(user_id=user_id, name=data['name'], phone_number=data['phone_number'])
        db.session.add(contact)
        db.session.commit()
        return {"message": "Contact added successfully."}, 201
