from flask_restx import Namespace, fields

api = Namespace('user', description='User operations')

user_model = api.model('User', {
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'address': fields.String(required=False, description='The user address'),
    'birthdate': fields.Date(required=False, description='The user birthdate'),
})

