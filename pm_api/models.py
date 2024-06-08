from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionManager
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class UserProfileManager(BaseUserManager):
    '''Manager for user profile'''
    def create_user(self, email, name, password=None):
        '''create a new user profile'''
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)  # this will encrypt password not just add the text value
        user.save(using=self._db)  # standard procedure for saving objects in django

        return user

    def create_super_user(self, email, name, password):
        '''create a new super user'''
        user = self.create_user(email, name, password)
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)  # standard procedure for saving objects in django

        return user



class UserProfile(AbstractBaseUser,
                  PermissionManager
):
    '''Database model for users in the system'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'  # override username as email
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        '''Returns full name of user'''
        return self.name
    
    def __str__(self):  # recommended for all django models
        '''returns string representation of user model'''
        return self.email
