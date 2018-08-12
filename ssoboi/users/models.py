from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group, User
# Create your models here.


class MyUser(User):
    phone_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return str(self.first_name + self.last_name)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, isStaff=False):
        """
        Creates, saves and adds to special group a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        if isStaff:
            group = Group.objects.get(name='staff')
        else:
            group = Group.objects.get(name='users')
        group.user_set.add(user)
        user.save(using=self._db)
        group.save(using=self._db)
        return user


