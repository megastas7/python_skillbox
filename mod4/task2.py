from typing import Optional
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        length_data = len(str(field.data))
        if length_data < self.min or length_data > self.max:
            raise ValidationError(self.message)


def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(field: Field):
        if len(str(field.data)) > max or len(str(field.data)) < min:
            raise ValidationError(message)
    return _number_length