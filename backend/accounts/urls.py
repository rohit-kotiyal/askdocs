from django.urls import path
from .views import RegisterView, MeView, InviteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),


    path("register/", RegisterView.as_view(), name="register"),
    path("invite/", InviteView.as_view(), name="invite"),
]
