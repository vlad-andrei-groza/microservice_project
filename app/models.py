from .db import db
from datetime import datetime
from pydantic import BaseModel, Field
from werkzeug.security import generate_password_hash, check_password_hash


class PowRequest(BaseModel):
    base: int
    exponent: int


class FibonacciRequest(BaseModel):
    n: int = Field(..., ge=0)


class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0)


class ResultResponse(BaseModel):
    result: int | float


class MathOperationRequest(db.Model):
    __tablename__ = 'math_operations'

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    input = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<MathOperationRequest {self.id} - {self.operation}({self.input}) = {self.result}>"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
