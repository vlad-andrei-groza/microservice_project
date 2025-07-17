from .db import db
from datetime import datetime
from pydantic import BaseModel


class PowRequest(BaseModel):
    base: int
    exponent: int


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
