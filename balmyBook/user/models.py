from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import jwt
from django.conf import settings
from datetime import datetime, timedelta
import uuid
from helpers.models import TrackingModel

# Create your models here.

class CustomUserManager(BaseUserManager):
    """Manager for custom user model"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)    

        return user
        
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

    

class User(AbstractBaseUser, PermissionsMixin):
    "A class to create a system user"

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True,
        editable=False, 
        default=uuid.uuid4,
        verbose_name="Public Identifier"
    )
    first_name = models.CharField(max_length=30, blank=False)
    second_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    username = models.CharField(max_length=30, blank=False, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    user_profile = models.CharField(max_length=100, blank=True)
    phone = models.CharField(blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'second_name', 'last_name', 'user_profile']

    def __str__(self):
        return self.first_name if self.first_name else self.uuid

    class Meta:
        verbose_name = "user"

    # Add generate_jwt_tokens to the User model
    def generate_jwt_tokens(self):
        """Generate access and refresh tokens for a user"""
        access_token = jwt.encode(
            {"email": self.email, "exp": datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY,
            algorithm="HS256"
        )

        refresh_token = jwt.encode(
            {"email": self.email, "exp": datetime.utcnow() + timedelta(hours=72)},
            settings.SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

