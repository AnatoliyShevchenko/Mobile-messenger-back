# Django
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator,
)

# Rest Framework
from rest_framework import status

# Third-Party
from typing import Any


VALIDATE_PATTERN = r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%&:;()*_\-])[a-zA-Z0-9!@#$%&:();*_\-]+$"""
PASSWORD_MESSAGE = """password must contain only latin character(upper and lower register), symbols and numbers"""
USERNAME_MESSAGE = """username must contain only latin character(upper and lower register), symbols and numbers"""
PASSWORD_LENGTH_MESSAGE = "length password must be 10-32 symbols"
USERNAME_LENGTH_MESSAGE = "length username must be 10-32 symbols"
PHONE_REGEX = r'^\+\d{1,3}-\d{1,3}-\d{3,14}$'
PHONE_ERROR = 'enter correct number in format +X-XXX-XXXXXXXXXXXX'
USERNAME_VALIDATOR = [
    RegexValidator(
        regex=VALIDATE_PATTERN,
        message=USERNAME_MESSAGE
    ),
    MinLengthValidator(
        limit_value=10,
        message=USERNAME_LENGTH_MESSAGE
    ),
    MaxLengthValidator(
        limit_value=32,
        message=USERNAME_LENGTH_MESSAGE
    ),
]
PASSWORD_VALIDATOR = [
    RegexValidator(
        regex=VALIDATE_PATTERN,
        message=PASSWORD_MESSAGE
    ),
    MinLengthValidator(
        limit_value=10,
        message=PASSWORD_LENGTH_MESSAGE
    ),
    MaxLengthValidator(
        limit_value=32,
        message=PASSWORD_LENGTH_MESSAGE
    ),
]

STATUS_CODES: dict[str, Any] = {
    '500': status.HTTP_500_INTERNAL_SERVER_ERROR,
    '404': status.HTTP_404_NOT_FOUND,
    '403': status.HTTP_403_FORBIDDEN,
    '400': status.HTTP_400_BAD_REQUEST,
    '202': status.HTTP_202_ACCEPTED,
    '200': status.HTTP_200_OK,
}

