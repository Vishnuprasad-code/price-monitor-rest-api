from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from price_monitor_project import settings

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

    def create_superuser(self, email, name, password):
        '''create a new super user'''
        user = self.create_user(email, name, password)
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)  # standard procedure for saving objects in django

        return user



class UserProfile(
    AbstractBaseUser,
    PermissionsMixin
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

    def get_short_name(self):
        '''Returns full name of user'''
        return self.name

    def __str__(self):  # recommended for all django models
        '''returns string representation of user model'''
        return self.email


class Product(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.url


class PriceHistory(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=3)
    last_updated = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_price_histories',
    )

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return f'Price is {self.price} as of {self.last_updated}'
    

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_wishlist_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_on']

    def __str__(self):
        return f'Wishlist of {self.user.name} product: {self.product.url}'