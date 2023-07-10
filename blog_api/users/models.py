from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers for authentication instead of usernames.
    """

    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        err_msg = "Users must have {}"
        if not last_name:
            raise ValueError(err_msg.format("last name"))
        elif not first_name:
            raise ValueError(err_msg.format("first name"))
        elif not username:
            raise ValueError(err_msg.format("username"))
        elif not email:
            raise ValueError(err_msg.format("email"))
        elif not password:
            raise ValueError(err_msg.format(password))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_admin", True)

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **other_fields
        )

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    def __str__(self):
        return str(self.email)

    @property
    def is_staff(self):
        return self.is_admin
