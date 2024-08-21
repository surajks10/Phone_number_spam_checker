from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models import User, Contact, SpamReport, db

# Report Spam
class ReportSpam(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number', type=str, required=True)

    @jwt_required()
    def post(self):
        data = ReportSpam.parser.parse_args()
        user_id = get_jwt_identity()
        report = SpamReport(phone_number=data['phone_number'], reported_by=user_id)
        db.session.add(report)
        db.session.commit()
        return {"message": "Number reported as spam."}, 201

# Search
class SearchByName(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)

    @jwt_required()
    def get(self):
        data = SearchByName.parser.parse_args()
        query = data['name']
        results = []

        # Names starting with the query
        users = User.query.filter(User.name.like(f'{query}%')).all()
        contacts = Contact.query.filter(Contact.name.like(f'{query}%')).all()

        for user in users:
            results.append({"name": user.name, "phone_number": user.phone_number, "spam_likelihood": self.calculate_spam_likelihood(user.phone_number)})

        for contact in contacts:
            results.append({"name": contact.name, "phone_number": contact.phone_number, "spam_likelihood": self.calculate_spam_likelihood(contact.phone_number)})

        # Names containing but not starting with the query
        users = User.query.filter(User.name.like(f'%{query}%')).filter(User.name.notlike(f'{query}%')).all()
        contacts = Contact.query.filter(Contact.name.like(f'%{query}%')).filter(Contact.name.notlike(f'{query}%')).all()

        for user in users:
            results.append({"name": user.name, "phone_number": user.phone_number, "spam_likelihood": self.calculate_spam_likelihood(user.phone_number)})

        for contact in contacts:
            results.append({"name": contact.name, "phone_number": contact.phone_number, "spam_likelihood": self.calculate_spam_likelihood(contact.phone_number)})

        return results, 200

    def calculate_spam_likelihood(self, phone_number):
        total_reports = SpamReport.query.filter_by(phone_number=phone_number).count()
        if total_reports == 0:
            return 0
        return min(100, total_reports * 10)  # Example spam likelihood calculation

class SearchByPhoneNumber(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number', type=str, required=True)

    @jwt_required()
    def get(self):
        data = SearchByPhoneNumber.parser.parse_args()
        phone_number = data['phone_number']
        user = User.query.filter_by(phone_number=phone_number).first()
        contacts = Contact.query.filter_by(phone_number=phone_number).all()
        results = []

        if user:
            results.append({"name": user.name, "phone_number": user.phone_number, "spam_likelihood": self.calculate_spam_likelihood(phone_number)})

        for contact in contacts:
            results.append({"name": contact.name, "phone_number": contact.phone_number, "spam_likelihood": self.calculate_spam_likelihood(contact.phone_number)})

        return results, 200
