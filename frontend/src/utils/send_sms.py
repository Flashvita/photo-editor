import requests
import json
from app_settings.settings import CORS_ORIGIN


def send_sms(phone_number):
        """Sending sms to user device for completed registration
        """
        url = f'{CORS_ORIGIN}api/v1/account/send-sms'
                
        data = {
            "phone_number": phone_number
        }
        response = requests.post(url, data=json.dumps(data))
        
        data = json.loads(response.content)
        return data