class DevelopmentConfig(object):
    SECRET_KEY = 'Change it dwfsfscvsvsefdafqfqdqdqwfe'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tpm_service.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_APP_NAME = "TPM Service App"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False
    #REMEMBER_COOKIE_DURATION = 20 #seconds