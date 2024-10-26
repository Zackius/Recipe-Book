from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings
from user.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        print(auth_header, "NDO HOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

        if not auth_header:
            return None 
        
        try:
            auth_data = auth_header.decode("utf-8")
            auth_token = auth_data.split(" ")            
            if len(auth_token) != 2 or auth_token[0].lower() != 'bearer':
                raise exceptions.AuthenticationFailed("Token not valid")
            
            token = auth_token[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            username = payload.get("username")
            if not username:
                raise exceptions.AuthenticationFailed("Token payload missing 'username'")
            
            user = User.objects.get(username=username)
            return (user, token)
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired, please log in again.")
        
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token. Please log in again.")
        
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No user matching this token was found.")
        
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Authentication failed: {str(e)}")
