from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

# Define a simple route for the API
@api_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"})
