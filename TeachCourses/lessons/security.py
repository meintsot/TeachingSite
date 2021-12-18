from django.core.validators import validate_email, ValidationError
from django.contrib.auth.models import User
import random
import string

def get_random_password(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def check_email(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True

def get_user(username):
    user = User.objects.get(username=username)
    return user
