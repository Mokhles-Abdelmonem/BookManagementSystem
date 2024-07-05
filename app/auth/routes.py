from flask_jwt_extended.exceptions import WrongTokenError
from flask_restx import Resource
from flask import request, abort
from app import db, bcrypt
from app.auth.namespace import api, login_model
from app.auth.schemas import UserLoginSchema
from app.middlewares import validate
from app.models.token import TokenBlocklist
from app.models.user import User
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, get_jwt_header,
    get_jti
)


@api.route('/login')
class UserLogin(Resource):
    @validate(request_model=UserLoginSchema)
    @api.expect(login_model)
    @api.doc("login")
    def post(self, **kwargs):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            refresh_token_jti = get_jti(refresh_token)
            user.refresh_token_jti = refresh_token_jti
            db.session.commit()
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401


@api.route('/refresh')
class RefreshToken(Resource):

    @validate()
    @jwt_required(refresh=True)
    @api.doc("refresh")
    def post(self, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        refresh_token_jti = get_jwt()['jti']
        if user.refresh_token_jti != refresh_token_jti:
            return {'message': 'Invalid refresh token'}, 401
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200


@api.route('/logout')
class UserLogout(Resource):

    @validate()
    @jwt_required()
    @api.doc("logout")
    def post(self, **kwargs):
        jti = get_jwt()['jti']
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return {'message': 'Successfully logged out'}, 200
