from rest_framework import serializers

from pm_api import models

class HelloSerializer(serializers.Serializer):
    '''Serializes a name field for testing our APIview'''
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    '''Seliarises a UserProfile model'''

    class Meta:
        model = models.UserProfile  # set UserProfileSerializer to point to UserProfile model
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
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name']
            password=validated_data['password']
        )
        return user
