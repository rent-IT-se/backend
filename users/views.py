import jwt
from django.urls import reverse
from rest_framework import generics, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    EmailVerificationSerializer,
    GoogleSocialAuthSerializer,
    UserListSerializer,
)
from .permissions import (
    IsClient,
    IsSuperUser,
)
from .utils import Util
from rentit import settings
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from rest_auth.registration.views import SocialConnectView, SocialLoginView
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2")
)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user_data = serializer.data

            user = User.objects.get(email=user_data["email"])
            token = RefreshToken.for_user(user)
            current_site = request.get_host()
            link = reverse("email_verify")
            url = "http://" + current_site + link + "?token=" + str(token)
            body = "Hi " + " Use the link below to verify your email \n" + url
            data = {
                "email_body": body,
                "to_email": user.email,
                "email_subject": "Verify your email",
            }

            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        user = User.objects.get(id=payload["user_id"])
        try:
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(
                    {"email": "Successfully activated"}, status=status.HTTP_200_OK
                )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": "You successfully logged in",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=2)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    # permission_classes = (IsSuperUser,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class SupportViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=1)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = UserListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
