from flask import request
import flask_login
from app import app, db
from app import login_manager
from flask_restful import Resource
from passlib.hash import pbkdf2_sha256

class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    #active means enable
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    # User Authentication fields
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    roles = db.relationship('Role', secondary='user_roles')
    _is_authenticated = True

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value

    def hash_password(self, password):
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')) 
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


def user_register(username, password):
    if not User.query.filter(User.username == username).first():
        app.logger.info("add user {0}".format(username))
        user = User(username = username)
        user.password = user.hash_password(password)
        db.session.add(user)
        db.session.commit()

#reloading a user from the session(client use cookies)
@login_manager.user_loader
def user_loader(user_id):
    print(user_id)
    user = User.query.get(user_id)
    if user and user.is_active:
        return user
    else:
        return None

#support for username:password auth; Basic Auth; api_key Auth
@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if not User.query.filter(User.username == username).first():
        return

    user = User.query.filter(User.username == username).first()
    if user.verify_password(request.form['password']):
        user.is_authenticated = True
    else:
        user.is_authenticated = False
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return {
            "Message":"Login required", 
            "login":"tpm-api/login",
            "register":"tpm-api/register",
            "logout":"tpm-api/logout"
            }, 401

class User_Login(Resource):
    def post(self):
        #not safe use midle var and plaintext
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            abort(405, message="Input params not right") 
        user = User.query.filter(User.username == username).first()
        if not user:
            abort(400, message="User not exist")
        if user.verify_password(password):
            flask_login.login_user(user, False)
            return {"Message":"Login success"}, 200
        else:
            abort(405, message="Wrong password")    

class User_Logout(Resource):
    @flask_login.login_required
    def post(self):
        flask_login.logout_user()
        return "Logout success!"

class User_Register(Resource):
    def get(self):
        return {"Message":"User Register"}

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')#hash ?
        if User.query.filter_by(username=username).first() is not None: 
            abort(400, message="User exist")
        user_register(username, password) #except handle, user exist check
        return {"Message":"Register success!", "Username":username}, 201
