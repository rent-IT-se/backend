from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from orders.models import Cart


class SuperUser(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("role", 1)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")
        if other_fields.get("is_active") is not True:
            raise ValueError("Superuser must be assigned to is_active=True")
        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email")

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        Cart.objects.create(user=user)

        return user


AUTH_PROVIDERS = {'google': 'google',
                  'email': 'email',}


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        (1, "Support"),
        (2, "Client"),
    )
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)
    birth_date = models.DateField(null=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    front_pictures = models.ImageField(blank=True, null=True, upload_to='images/')
    back_pictures = models.ImageField(blank=True, null=True, upload_to='images/')
    face_pictures = models.ImageField(blank=True, null=True, upload_to='images/')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"

    objects = SuperUser()

    def __str__(self):
        return f"{self.email}"
