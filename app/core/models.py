from django.db import models
# We'll need some classes to extend the django user model that comes out of
# the box, whilst using some of the features that come by default
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):
    """ Provides the helper functions for creating a user or creating a superuser
    To achieve that goal we will override some functions of the BaseUserManager
    to handle our e-mail address instead of the user name that he expects"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User
        Note: password=None in case you want to create a user that is not
        active, that is, it doesn't have a password.
        Note: **extra_fields is included so that any fields added to our user
        it means we don't have to add them in here. They're added ad hoc as we
        add them to the model
        Note: normalize_email comes with the BaseUserManager"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # The password needs to be encrypted using django BaseUserManager's
        # set_password so it can't come from the **extra_fields
        user.set_password(password)
        user.save(using=self._db)
        # The self._db is required for supporting multiple databases

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """We need a custom user model that supports using email instead of
    username.
    Note: Extends the classes AbstractBaseUser, PermissionsMixin for us to
    customize it to support our email address"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # By default, the username is 'email'
    USERNAME_FIELD = 'email'
