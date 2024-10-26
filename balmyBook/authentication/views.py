from django.shortcuts import render
from user.models import User
from rest_framework.generics import GenericAPIView
from rest_framework import response, status
from django.contrib.auth import authenticate

# Create your views here.

class UserLoginView(GenericAPIView):
    """This service is meant to log in a single user to the system"""
    
    authentication_classes = []
    
    def post(self, request):
        try:
            incoming_data = request.data
            email = incoming_data.get("email", None)  # Use email, not username
            password = incoming_data.get("password", None)
            
            print(email, "Here is the email")
            user = None
            
            if email:
                user_required = User.objects.filter(email=email).first()  # Use email to find user
                print(user_required, "DONE!!!!!!!!!!!!!")
                
                if not user_required:
                    return response.Response(
                        {"msg": "User not present"}, 
                        status=status.HTTP_404_NOT_FOUND,
                    )
                else:
                    user = authenticate(email=email, password=password)  # Use email for authentication
                    print(user, "HERE IS THE USER >>>>>>>>>>>>>")
            
            if user:
                tokens = user.generate_jwt_tokens()
                logged_in_user = User.objects.get(id=user.id)  # Correct the query for the user object
                data = {
                    "first_name": logged_in_user.first_name,
                    "second_name": logged_in_user.second_name,
                    "last_name": logged_in_user.last_name,
                    "username": logged_in_user.username,
                    "email": logged_in_user.email,
                    "phone": logged_in_user.phone, 
                    "token": tokens
                } 
                return response.Response(
                    {"msg": "Success", "data": data},
                    status=status.HTTP_200_OK
                ) 
            else:
                return response.Response(
                    {"message": "Invalid credentials, try again."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        
        except Exception as e:
            return response.Response(
                {"msg": f"An error occurred while logging in user: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )