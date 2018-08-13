from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group, User
from phonenumber_field.modelfields import PhoneNumberField


class User(User):
    phone_number = PhoneNumberField()

    def __str__(self):
        return str(self.first_name + self.last_name)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False):
        """
        Creates, saves and adds to special group a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        if is_staff:
            group = Group.objects.get(name='staff')
        else:
            group = Group.objects.get(name='users')
        group.user_set.add(user)
        user.save(using=self._db)
        group.save(using=self._db)
        return user


