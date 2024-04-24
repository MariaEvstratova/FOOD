from flask import jsonify

from . import db_session
from .users import User
from flask_restful import reqparse, abort, Api, Resource


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'about', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'about', 'email', 'hashed_password')) for item in users]})

    def post(self):
        parser = reqparse.RequestParser ()
        parser.add_argument ('name', required=True)
        parser.add_argument ('about', required=True)
        parser.add_argument ('email', required=True, type=str)
        parser.add_argument ('hashed_password', required=True, type=str)

        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            name=args['name'],
            about=args['about'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})