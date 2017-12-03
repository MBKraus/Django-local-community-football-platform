from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from django.core import validators

POSITION_CHOICES = (
    (0, "Keeper"),
    (1, "Defence"),
    (2, "Midfield"),
    (3, "Attack")
)

MEMBERSHIP_CHOICES = (
    (0, "banned"),
    (1, "member"),
    (2, "moderator"),
    (3, "admin")
)

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):

        if not email:

            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email,
            username,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.role = 3
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(('username'), max_length=30, unique=True,
                                help_text=('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', ('Enter a valid username.'), 'invalid')
                                ])
    bio = models.CharField(max_length=140, blank=True, default="")
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(default=datetime.now, blank=True)
    role = models.IntegerField(choices=MEMBERSHIP_CHOICES, default=1)
    is_staff = models.BooleanField(default=False)
    position = models.IntegerField(choices=POSITION_CHOICES, default=1)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return "{}".format(self.username)

    def get_short_name(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})