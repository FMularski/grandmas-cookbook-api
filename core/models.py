from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    TYPE_BRONZE = "B"
    TYPE_SILVER = "S"
    TYPE_GOLDEN = "G"

    TYPE_CHOICES = (
        (TYPE_BRONZE, _("Bronze")),
        (TYPE_SILVER, _("Silver")),
        (TYPE_GOLDEN, _("Golden")),
    )

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_BRONZE)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
