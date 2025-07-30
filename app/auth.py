import os

import jwt
from flask import request, jsonify
from datetime import datetime, timedelta

from app.db import db
from app.models import User
from flask import Blueprint


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        payload = {
            "user_id": user.id,
            "exp": datetime.now() + timedelta(hours=1)
        }
        token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
        return jsonify(access_token=token)
    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=data["username"], role=data.get("role", "user"))
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
