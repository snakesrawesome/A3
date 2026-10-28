from flask import Flask, jsonify, request,g
from flask_restful import Resource, Api, reqparse
from flask_talisman import Talisman
from cs188_a3.db import Database
from flask_bcrypt import Bcrypt

def get_db() -> Database:
    if "db" not in g:
        g.db = Database()
    return g.db


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth is None:
            return jsonify({"message": "Authentication required"}), 401
        db = get_db()
        hashed_pwd = db.get_password(auth.username)
        valid = hashed_pwd is not None and Bcrypt().check_password_hash(hashed_pwd, auth.password)
        if not valid:
            return jsonify({"message": "Invalid credentials"}), 401
        g.username = auth.username
        return func(*args, **kwargs)
    return wrapper


def init_api(app: Flask)->None:
    api = Api(app)
    api.add_resource(Hello, '/')
    api.add_resource(Square, "/square/<int:num>") 
    api.add_resource(Echo, "/echo")
    api.add_resource(Register, "/register")
    api.add_resource(Profile, "/profile")

def create_app()-> Flask:
    app = Flask(__name__)
    app.config["PREFERRED_URL_SCHEME"] = "https"
    Talisman(app, force_https=True)
    init_api(app)
    return app

def run_app(debug: bool=True,with_ssl=True)->None:
    ssl_context = (_CERTIFICATE_PATH, _KEYFILE_PATH) if with_ssl else None
    create_app().run(debug=debug,ssl_context=ssl_context)

if __name__ == "__main__":
    run_app()

class Square(Resource):
    def get(self, num):
        return jsonify({'Shape': __class__.__name__,'Area': num*num})


class Echo(Resource):
    # Use RequestParser to parse the arguments from the request.
    # Don't reinvent the wheel! We could write a parser ourselves,
    # but let's use one that was already made for us!
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('arg1', type=str, location='args')
        parser.add_argument('arg2', type=str, location='args')
        arguments = parser.parse_args()
        # Return the arguments as JSON
        return jsonify(arguments)

_KEYFILE_PATH = os.path.join(PROJECT_ROOT, "MyKey.pem")
_CERTIFICATE_PATH = os.path.join(PROJECT_ROOT, "MyCertificate.crt")

