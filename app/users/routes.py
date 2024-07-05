from flask_restx import Resource
from flask import request
from app import db, bcrypt
from app.middlewares import validate
from app.models.token import TokenBlocklist
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.users.namespace import api, user_model
from app.users.schemas import UserIn, UserOut


@api.route('/register')
class UserRegister(Resource):
    @validate(request_model=UserIn, response_model=UserOut)
    @api.expect(user_model)
    @api.doc("register")
    def post(self, **kwargs):
        request_model: UserIn = kwargs['request_model']
        if User.query.filter_by(email=request_model.email).first():
            return {'message': 'User already exists'}, 400

        hashed_password = bcrypt.generate_password_hash(request_model.password).decode('utf-8')
        new_user = User(
            username=request_model.username,
            email=request_model.email,
            password=hashed_password,
            address=request_model.address,
            birthdate=request_model.birthdate
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user.to_dict(), 201


@api.route('/me')
class UserMe(Resource):
    @validate(response_model=UserOut)
    @jwt_required()
    @api.doc("me")
    def get(self, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user.to_dict()

    @validate(request_model=UserIn, response_model=UserOut)
    @api.doc("update_user")
    @api.expect(user_model)
    @jwt_required()
    def put(self, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        if data["email"] != user.email:
            users = User.query.filter(User.email == data["email"]).all()
            if users:
                return {'message': 'this email exists'}, 401
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user.to_dict()

    @validate()
    @api.doc("delete_user")
    @api.response(204, 'User deleted')
    @jwt_required()
    def delete(self, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        jti = get_jwt()['jti']
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return {'message': 'User deleted successfully'}, 204


@api.route('/list')
class UserList(Resource):
    @validate(response_model=UserOut, is_list=True)
    @api.doc("get_users")
    @jwt_required()
    def get(self, **kwargs):
        users = User.query.all()
        return users
