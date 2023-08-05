from flask_restful import abort

def abort_if_todo_doesnt_exist(todo_id, todo_list):
    if todo_id not in todo_list:
        abort(404, message="TPM action {} doesn't exist".format(todo_id))

def abort_if_mimetype_not_json():
    if not request.json:
        abort(400, message="Content-Type must json")

def abort_if_input_doesnt_right(inputs, todo_id):
    if not tpm_input_validate.get(todo_id)(inputs):
        abort(405, message="Input params not right")

def validate_tpm_hash(inputs):
    if not 'ic' in input:
        return False

tpm_input_validate = {
    'validate_tpm_hash' : validate_tpm_hash
}
