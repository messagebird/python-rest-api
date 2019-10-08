from messagebird.error import ValidationError


def validate_is_not_blank(value, message):
    if value is None or not value.strip():
        raise ValidationError(message)
