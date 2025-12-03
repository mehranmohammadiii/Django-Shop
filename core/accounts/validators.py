from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    """
    Validate Iranian phone number format.
    Accepts format: 09xxxxxxxxx (11 digits)
    """
    # Remove spaces and dashes
    phone = value.replace(" ", "").replace("-", "")
    
    # Pattern for Iranian phone numbers
    pattern = r'^09\d{9}$'
    
    if not re.match(pattern, phone):
        raise ValidationError(
            'شماره تلفن نامعتبر است. لطفا فرمت 09xxxxxxxxx را استفاده کنید.',
            code='invalid_phone'
        )
    
    return phone
# -----------------------------------------------------------------------------------------