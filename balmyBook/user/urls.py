from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("user/register", views.CreateSystemUser.as_view(), name="new user"),
    
]
