"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, TokenBlockedList
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt



api = Blueprint('api', __name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Allow CORS requests to this API
CORS(app)

@api.route('/signup', methods=['POST'])
def user_signup():
    body = request.get_json()

    if "email" not in body:
        return jsonify({"msg": "Email field is required"}), 400
    if "password" not in body:
        return jsonify({"msg": "Password field is required"}), 400

    existing_user = User.query.filter_by(email=body["email"]).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 400

    encrypted_password = bcrypt.generate_password_hash(body["password"]).decode('utf-8')

    new_user = User(
        email=body["email"],
        password=encrypted_password,
        is_active=True
    )

    if "first_name" in body:
        new_user.first_name = body["first_name"]
    else:
        new_user.first_name = ""

    if "last_name" in body:
        new_user.last_name = body["last_name"]
    else:
        new_user.last_name = ""

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@api.route('/login', methods=['POST'])
def user_login():
    body = request.get_json()
    
    if "email" not in body:
        return jsonify({"msg": "Email field is required"}), 400
    
    if "password" not in body:
        return jsonify({"msg": "Password field is required"}), 400
    
    user = User.query.filter_by(email=body["email"]).first()
    
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    
    if not bcrypt.check_password_hash(user.password, body["password"]):
        return jsonify({"msg": "Invalid password"}), 401
    
    role = "admin" if user.id % 2 == 0 else "user"
    
    token = create_access_token(identity=user.id, additional_claims={"role": role})
    
    return jsonify({"token": token}), 200

@api.route('/userinfo', methods=['GET'])
@jwt_required()
def user_info():
	user=get_jwt_identity()
	payload=get_jwt()
	return jsonify({"user":user,"role":payload["role"]})

@api.route('/logout', methods=["POST"])
@jwt_required()
def user_logout():
	jti=get_jwt()["jti"]
	token_blocked=TokenBlockedList(jti=jti)
	db.session.add(token_blocked)
	db.session.commit()
	return jsonify({"msg":"session finished"})

@api.route('/private', methods=['GET'])
@jwt_required()
def user_private():
    user=get_jwt_identity()
    return jsonify({"msg": "Access granted", "body": user})
