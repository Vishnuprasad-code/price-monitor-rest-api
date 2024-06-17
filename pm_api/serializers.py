from rest_framework import serializers

from pm_api import models

class HelloSerializer(serializers.Serializer):
    '''Serializes a name field for testing our APIview'''
    name = serializers.CharField(max_length=10)


class UserProfileModelSerializer(serializers.ModelSerializer):
    '''Seliarizes a UserProfile model'''

    class Meta:
        model = models.UserProfile  # set UserProfileModelSerializer to point to UserProfile model
        fields = ('id', 'email', 'name', 'password')
        # need to make password write only
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    # override default create
    def create(self, validated_data):
        '''Create and return a new user'''
        '''this is requeired to override create to hash password and not store text value of password'''
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class ProductModelSerializer(serializers.ModelSerializer):
    '''Seliarizes a UserProfile model'''
    class Meta:
        model = models.Product  # set ProductModelSerializer to point to Product model
        fields = ('id', 'url', 'name')


class WishlistModelSerializer(serializers.ModelSerializer):
    '''Serializes a Wishlist model'''
    product = ProductModelSerializer(read_only=True)
    class Meta:
        model = models.Wishlist  # set WishlistModelSerializer to point to Product model
        fields = ('product', 'added_on')


class ProductHistorySerializer(serializers.Serializer):
    '''Serializes a name field for testing our APIview'''
    url = serializers.CharField(max_length=255)


class ProductHistoryModelSerializer(serializers.ModelSerializer):
    '''Serializes a Wishlist model'''
    product = ProductModelSerializer(read_only=True)
    class Meta:
        model = models.PriceHistory  # set WishlistModelSerializer to point to Product model
        fields = (
            'product',
            'price',
            'currency',
            'last_updated'
        )