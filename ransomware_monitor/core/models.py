from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Missing email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email,password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError("Super user must be true")

        if not extra_fields.get('is_staff'):
            raise ValueError("staff user must be true")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField('Email', unique=True)
    is_staff = models.BooleanField('Staff', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self) -> str:
        return str(self.email)

    objects = UserManager()
