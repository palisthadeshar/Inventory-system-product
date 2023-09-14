import re

import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumbers import NumberParseException


def validate_mobile_number(value):
    """
    To use this function you need to install phonenumbers package
    https://github.com/daviddrysdale/python-phonenumbers

    Without any packages eg:
    phone_number = models.CharField(
        max_length= 16,
        validators=[
            RegexValidator(
                regex=r'^+?1?\d{d,15}$',
                message='Phone number must be entered in the format '+123456789'.
            )
        ]
    )
    """
    try:
        phone_number = phonenumbers.parse(value, None)
        if phonenumbers.is_possible_number(
            phone_number
        ) and phonenumbers.is_valid_number(phone_number):
            return True
        else:
            raise ValidationError(("Please enter valid phone numbers"))
    except NumberParseException:
        raise ValidationError(
            _("Please enter phone number with country code, prefix must be +")
        )


def valid_emails(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validaterequired(value):
    if not value:
        raise ValidationError(("This field is requried"))
    return True


def validate_password(password):
    from django.contrib.auth.password_validation import validate_password

    validate_password(password)