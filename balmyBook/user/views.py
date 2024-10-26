from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from user.models import User
from user.serializers import FullUserAddSerializer
from helpers.utils import _check_if_valid_phone_number

class CreateSystemUser(GenericAPIView):
    """
    This is a class to create a User
    """

    authentication_classes = []

    def post(self, request):
        try:
            incoming_data = request.data
            full_add_serializer = FullUserAddSerializer(data=incoming_data)

            if full_add_serializer.is_valid():
                email = incoming_data.get("email")
                phone = incoming_data.get("phone")
                first_name = incoming_data.get("first_name")
                second_name = incoming_data.get("second_name")
                last_name = incoming_data.get("last_name")
                username = incoming_data.get("username").lower()
                password = incoming_data.get("password")
                confirm_password = incoming_data.get("confirm_password")

                # Validate phone number
                if phone:
                    phone = _check_if_valid_phone_number(phone)

                # Check if user exists by email or phone
                user_present = User.objects.filter(Q(email=email) | Q(phone=phone)).exists()
                if user_present:
                    return Response(
                        {"msg": "User with similar details already exists"},
                        status=status.HTTP_409_CONFLICT,
                    )

                # Check if username exists
                username_present = User.objects.filter(username=username).exists()
                if username_present:
                    return Response(
                        {"msg": "A user with similar details already exists"},
                        status=status.HTTP_409_CONFLICT,
                    )

                # Check if passwords match
                if confirm_password != password:
                    return Response(
                        {"msg": "Password Mismatch!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Create user details dictionary
                user_details = {
                    "first_name": first_name,
                    "second_name": second_name,
                    "last_name": last_name,
                    "username": username,
                    "email": email,
                    "phone": phone,
                    "password": make_password(password)
                }
                print(user_details, "DOneSS")

                # Serialize the user details
                user_serializer = FullUserAddSerializer(data=user_details)
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response(
                        {"msg": "User created successfully"},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        user_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                # In case the incoming data is invalid
                return Response(
                    full_add_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            # Ensure that any exception results in an error response
            return Response(
                {"msg": f"An error occurred while saving user: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fallback Response (in case of unexpected behavior)
        return Response(
            {"msg": "Unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
