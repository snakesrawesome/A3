from flask import jsonify, g
from flask_restful import Resource
from .services import auth_required

class Profile(Resource):
    @auth_required
    def get(self):
        return jsonify({"message": f"Hello, {g.username}!"})

# Create the "hello" resource
class Hello(Resource):
    # Get is a special method for a resource.
    def get(self):
        return jsonify({"message": "Hello World!"})

class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True,help="Username cannot be blank",)
        parser.add_argument("password", type=str, required=True,help="Password cannot be blank",)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        # Hash the password before storing it
        hashed_pwd = Bcrypt().generate_password_hash(password).decode('utf-8')
        db = get_db()
        if db.add_user(username, hashed_pwd):
            return jsonify({"message": f"User {username} registered successfully"})
        else:
            return jsonify({"message": f"User {username} already exists"}), 409
