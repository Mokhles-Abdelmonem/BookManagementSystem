from flask_restx import Namespace, fields

api = Namespace('auth', description='auth operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})
