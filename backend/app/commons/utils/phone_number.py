import phonenumbers


def validate_phone_number(number) -> bool:
    """Validate input phone number 
    """
    phone_number_obj = phonenumbers.parse(number, None)
    
    return phonenumbers.is_valid_number(phone_number_obj)