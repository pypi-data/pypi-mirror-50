"""
Put all functions here.
"""
import json
import subprocess
from app import app

tpm_tools_path = '/home/wenzt/tpm/ibm_tss/build/bin/'

def tpm_hash(input, halg='sha256'):

    cmd_line = [tpm_tools_path + 'tsshash']
    cmd_line.extend(['-ic', input['ic']])
    cmd_line.extend(['-halg', input.get('halg', 'sha256')])
    cmd_line.append('-ns')
    p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE)
    p.wait()

    rv = p.stdout.read().strip()
    return {'hash_result' : rv}

def tpm_startup(input):
    cmd_line = [tpm_tools_path + 'tssstartup']
    p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE)
    p.wait()

    rv = p.stdout.read().strip()
    return {'result' : rv}

#this dict define all methods that tpm/tpm_methods
tpm_action = [
    'tpm_startup',
    'tpm_hash'
]

#tpm action called by @GET @PUT @POST ...
tpm_action_handle = {
    'tpm_startup' : tpm_startup,
    'tpm_hash' : tpm_hash
}

#place here for now
tpm_services = [
    "actions",
    "policys",
    "register",
    "login",
    "logout",
]