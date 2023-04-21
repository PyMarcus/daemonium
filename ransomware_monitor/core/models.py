from typing import Optional, Any, List
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations: bool = True

    def _create_user(self, email: str, password: str, **extra_fields) -> Any:
        if not email:
            raise ValueError("Missing email address")
        email: str = self.normalize_email(email)
        user: Any = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> Any:
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> Any:
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError("superuser must be true")

        if not extra_fields.get('is_staff'):
            raise ValueError("staff user must be true")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email: str = models.EmailField('E-mail', unique=True)
    password: str = models.CharField('Phone', max_length=15)
    is_staff: bool = models.BooleanField('Staff', default=True)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['first_name', 'last_name']

    def __str__(self) -> str:
        return str(self.email)

    objects = UserManager()
