from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIClient

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')
        if not api_key or not api_key.startswith("Api-Key "):
            raise AuthenticationFailed("Missing or invalid API key.")

        key = api_key.split(" ")[1]
        try:
            client = APIClient.objects.get(api_key=key, is_active=True)
        except APIClient.DoesNotExist:
            raise AuthenticationFailed("Invalid API key.")

        return (client, None)