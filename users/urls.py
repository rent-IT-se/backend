from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework.routers import DefaultRouter
from rest_auth.views import (
    PasswordResetView, PasswordResetConfirmView
)
from .views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    GoogleSocialAuthView,
    ClientViewSet,
    UserViewSet,
    SupportViewSet,
    AdminViewSet,

)

users_router = DefaultRouter()

users_router.register(r'clients', ClientViewSet, basename='clients')
users_router.register(r'supports', UserViewSet, basename='supports')
users_router.register(r'admins', SupportViewSet, basename='admins')
users_router.register(r'all-users', AdminViewSet, basename='all-users')

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("obtain/", TokenObtainPairView.as_view()),
    path("api/register/email_verify/", VerifyEmailView.as_view(), name="email_verify"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("confirm-email/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="confirm-email"),
    path('google/', GoogleSocialAuthView.as_view()),
]
