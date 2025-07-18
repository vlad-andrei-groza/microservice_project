import flask
from flask import Blueprint, jsonify
from pydantic import ValidationError
from . import db
from .models import MathOperationRequest, PowRequest, ResultResponse, FibonacciRequest, FactorialRequest
from .operations import pow_func, fibonacci, factorial

api_bp = Blueprint('api', __name__)
math_operations_bp = Blueprint('math', __name__, url_prefix='/api/math')


# Define a simple route for the API
@api_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"})


@math_operations_bp.route('/pow', methods=['POST'])
def pow_operation_route():
    """
    Handle POST requests for power operation.
    :return: the result of the power operation as JSON
    """
    data = flask.request.get_json()
    parsed_data, errors = parse_request(PowRequest, data)
    if errors:
        return jsonify(errors=errors), 400
    base, exponent = parsed_data.base, parsed_data.exponent
    result = pow_func(base, exponent)
    store_request("pow", f"b={base}, e={exponent}", result)

    return jsonify(ResultResponse(result=result).model_dump())


@math_operations_bp.route('/pow', methods=['GET'])
def get_all_pow_operation_results():
    """
    Handle GET requests for power operation.
    :return: all power operation results as JSON
    """
    requests = (MathOperationRequest
                .query
                .filter_by(operation='pow').all())
    results = [
        {
            "id": req.id,
            "input": req.input,
            "result": req.result,
            "timestamp": req.timestamp.isoformat()
        } for req in requests
    ]

    return jsonify(results=results)


@math_operations_bp.route('/fibonacci', methods=['POST'])
def fibonacci_route():
    """
    Handle POST requests for Fibonacci operation.
    :return: the result of the Fibonacci operation as JSON
    """
    data = flask.request.get_json()
    parsed_data, errors = parse_request(FibonacciRequest, data)
    if errors:
        return jsonify(errors=errors), 400
    result = fibonacci(parsed_data.n)
    store_request("fibonacci", f"n={parsed_data.n}", result)

    return jsonify(ResultResponse(result=result).model_dump())


@math_operations_bp.route('/fibonacci', methods=['GET'])
def get_all_fibonacci_results():
    """
    Handle GET requests for Fibonacci operation.
    :return: all Fibonacci operation results as JSON
    """
    requests = (MathOperationRequest
                .query
                .filter_by(operation='fibonacci').all())
    results = [
        {
            "id": req.id,
            "input": req.input,
            "result": req.result,
            "timestamp": req.timestamp.isoformat()
        } for req in requests
    ]

    return jsonify(results=results)


@math_operations_bp.route('/factorial', methods=['POST'])
def factorial_route():
    """
    Handle POST requests for factorial operation.
    :return: the result of the factorial operation as JSON
    """
    data = flask.request.get_json()
    parsed_data, errors = parse_request(FactorialRequest, data)
    if errors:
        return jsonify(errors=errors), 400
    result = factorial(parsed_data.n)
    store_request("factorial", f"n={parsed_data.n}", result)

    return jsonify(ResultResponse(result=result).model_dump())


@math_operations_bp.route('/factorial', methods=['GET'])
def get_all_factorial_results():
    """
    Handle GET requests for factorial operation.
    :return: all factorial operation results as JSON
    """
    requests = (MathOperationRequest
                .query
                .filter_by(operation='factorial').all())
    results = [
        {
            "id": req.id,
            "input": req.input,
            "result": req.result,
            "timestamp": req.timestamp.isoformat()
        } for req in requests
    ]

    return jsonify(results=results)


# function to parse request data using Pydantic models
def parse_request(model, data):
    try:
        return model(**data), None
    except ValidationError as e:
        return None, e.errors()


def store_request(operation, input_data, result):
    """
    Store a math operation request in the database.
    :param operation: type of operation (e.g., "pow")
    :param input_data: input data for the operation
    :param result: result of the operation
    :return: ID of the stored request
    """
    request = MathOperationRequest(
        operation=operation,
        input=input_data,
        result=str(result)
    )
    db.session.add(request)
    db.session.commit()
    return request.id
