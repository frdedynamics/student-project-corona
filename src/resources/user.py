from flask_restful import Resource, reqparse

from src.models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Required field.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Required field.")

    def post(self):
        data = self.parser.parse_args()
        username = data['username']

        if UserModel.find_by_username(username):
            return {"message": f"User {username} already exists."}, 400

        user = UserModel(**data)
        user.save()

        return {"message": f"User {username} registered."}, 201


class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}

