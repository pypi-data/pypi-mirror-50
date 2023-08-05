""" 
Purpose:    Main file about TPM service restful api.
            This project aimed to provide a TPM service for APPs.
            They can get TPM functions by calling APIs provided by this service. 

Attention:  This code should not be used in product directly, it just for demo.
            I use Flask-Restful API framwork(https://github.com/flask-restful/flask-restful)
            to create REST API for TPM service.
            Method call C binary file directly is not recommanded but used for now.
            TSS was writen in C, so python-C binding may be needed like libvirt-python.
            Or use ctypes...

About TPM:  TPM sorftware stack is ibm_tss.
            TPM2.0 simulator is ibm_sim.
            TSS can be replaced by other like MSR TSS or TCG TSS.
            TPM2.0 may provided by hardware, simulator, CUSE vtpm device.
            Whatever TSS or TPM is decoupled from this API.

TODO:       ACL and https, user mangement, requestParse

For test: 
            #/: curl -v -X PUT -H "Content-Type: application/json" -d '{"ic":"222"}' http://127.0.0.1:5000/tpm/tpm_hash
            return:
            {
                "hash_result": "9b871512327c09ce91dd649b3f96a63b7408ef267c8cc5710114e629730cb61f"
            }
"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import flask_login
import logging

app = Flask("TPM_Service_APP")
app = Flask(__name__.split('.')[0])
api = Api(app, default_mediatype='application/json')
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.login_message = "Login required"
app.logger.setLevel(logging.DEBUG)