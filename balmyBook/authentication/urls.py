        from django.urls import path
from . import views

urlpatterns = [
    path("auth/login", views.UserLoginView.as_view(), name="login")
]
