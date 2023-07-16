import phonenumbers


def validate_phone_number(number):
        """
        Checking input number by valid Google's libphonenumber library 
        #https://pypi.org/project/phonenumbers/
        """
        try:
            obj_phone_number = phonenumbers.parse(number, None)  
            return phonenumbers.is_valid_number(obj_phone_number)
        except:
            return False
        
def error_input_number(self):
    self.phone_number.error_text = 'Неправильный формат номера телефона'
    self.phone_number.update()