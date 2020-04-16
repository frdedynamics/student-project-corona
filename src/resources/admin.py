from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from src.models.admin import AdminModel
from src.models.user import UserModel


class Admin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('access_level',
                        type=int,
                        required=True,
                        help="Required field.")

    @jwt_required()
    def post(self, username):
        data = self.parser.parse_args()
        required_access = 3
        current_user = current_identity  # type: UserModel
        admin = AdminModel.find_by_id(current_user.id)
        if not admin:
            return {'message': 'No admin access.'}, 400

        if admin.access_level < required_access:
            return {'message': f'Access level {required_access} required.'}, 400

        other_user = UserModel.find_by_username(username)

        if not other_user:
            return {'message': f'User {username} doesn\'t exist.'}, 400

        if other_user.is_admin():
            return {'message': f'User {username} is already admin.'}, 400

        access_level = data['access_level']
        if admin.access_level <= access_level:
            return {'message': 'Access level must be lower than self.'}, 400

        if access_level < 1:
            return {'message' 'Invalid access level.'}, 400

        new_admin = AdminModel(other_user.id, access_level)
        new_admin.save()
        return {'admin': new_admin.json()}, 201
