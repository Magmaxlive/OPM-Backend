from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        
        try:
            validated = self.get_validated_token(token)
            user = self.get_user(validated)
            return (user, validated)
        
        except (InvalidToken, TokenError):
            return None
       