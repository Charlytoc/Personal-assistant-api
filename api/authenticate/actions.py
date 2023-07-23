import string
import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Token

def get_or_create_valid_token(user: User):
    try:
        # Try to get an existing token for the user
        token = Token.objects.get(user=user, expiration_date__gt=timezone.now())
    except Token.DoesNotExist:
        # If no valid token exists, create a new one
        token = Token(user=user)
        token.save()

    return token

# Example usage:
# Assuming you have a user object (e.g., user = User.objects.get(username='example_user'))
# you can call the function to get or create a valid token for that user:
# token = get_or_create_valid_token(user)
# Now 'token' will contain the valid token associated with the user, or a newly created one if it didn't exist before.
