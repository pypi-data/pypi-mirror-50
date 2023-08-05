from flask import request
from flask_restful import Resource, fields, marshal_with
import flask_login, tpm_utils
from tpm_actions import tpm_action, tpm_services
from usage import tpm_usage
from app import api
from auth import User_Login, User_Logout, User_Register
from app import app

api_resource_field = {
    'apiKey': fields.String,
    'apiUrl': fields.Url('service_ep', True)
}

service_resource_field = {
    'total': fields.Integer,
    'apis': fields.List(fields.Nested(api_resource_field))      
}

action_field = {
    'desc': fields.String,
    'apiKey': fields.String,
    'apiUrl': fields.Url('action_ep', True)
}
actions_resource_field = {
    'total': fields.Integer,
    'apis': fields.List(fields.Nested(action_field))
}

action_handle_field = {
    'desc': fields.String,
    'usage': fields.List(fields.String)
}

class Tpm_service_list(Resource):
    @marshal_with(service_resource_field)
    def get(self):
        data = {'total':len(tpm_services)}
        apis = []
        for v in tpm_services:
            apis.append({'apiKey': v, 'service_id': v})
        data['apis'] = apis
        return data

class Tpm_service(Resource):
    def get(self, service_id):
        tpm_utils.abort_if_todo_doesnt_exist(service_id, tpm_services)
        pass

class Tpm_action_list(Resource):
    @marshal_with(actions_resource_field)
    def get(self):
        data = {'total':len(tpm_action)}
        apis = []
        for v in tpm_action:
            apis.append({'apiKey': v, 'desc': tpm_usage.get(v).get('description'), 'action_id': v})
        data['apis'] = apis
        return data

class Tpm_action(Resource):
    @flask_login.login_required
    def get(self, action_id):
        tpm_utils.abort_if_todo_doesnt_exist(action_id, tpm_action)
        return tpm_usage.get(action_id)

    def put(self, action_id):
        tpm_utils.abort_if_todo_doesnt_exist(action_id, tpm_action)
        tpm_utils.abort_if_mimetype_not_json()
        input = request.get_json()
        #TODO: validate should replaced by RequestParser 
        tpm_utils.abort_if_input_doesnt_right(input, action_id)
        return tpm_action_handle.get(action_id)(input)

class Tpm_policy_list(Resource):
    def get(self):
        pass

class Tpm_policy(Resource):
    def get(self, todo_id):
        pass

    def put(self, todo_id):
        pass
def views_init():
    api.add_resource(Tpm_service_list, '/tpm-api')
    api.add_resource(Tpm_service,'/tpm-api/<service_id>', endpoint = 'service_ep')

    api.add_resource(Tpm_action_list, '/tpm-api/actions', endpoint = 'actions_ep')
    api.add_resource(Tpm_action, '/tpm-api/actions/<action_id>', endpoint = 'action_ep')

    api.add_resource(Tpm_policy_list, '/tpm-api/policys', endpoint = 'policys_ep')
    api.add_resource(Tpm_policy, '/tpm-api/policys/<policys_id>', endpoint = 'policy_ep')

    api.add_resource(User_Login, '/tpm-api/login', endpoint = 'login_ep')
    api.add_resource(User_Logout, '/tpm-api/logout', endpoint = 'logout_ep')
    api.add_resource(User_Register, '/tpm-api/register', endpoint = 'register_ep')