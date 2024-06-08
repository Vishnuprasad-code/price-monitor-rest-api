from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


from pm_api import models
from pm_api import serializers

from django.contrib.auth import get_user_model


class HelloApiView(APIView):
    '''Test API view'''

    serializer_class = serializers.HelloSerializer
    def get(self, request, format=None):
        '''Returns a list of APIView features'''
        an_api_view = [
            "World"
        ]
    
        return Response(
            {'message': 'Hello'}
        )

    def post(self, request):
        '''create a hello message with name'''
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response(message)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileSignUpView(APIView):
    serializer_class = serializers.UserProfileSerializer

    def post(self, request, format=None):
        user_profile_serializer = self.serializer_class(data=request.data)
        if not user_profile_serializer.is_valid():
            return Response(
                user_profile_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_profile_serializer.save()
        user = get_user_model().objects.get(email=request.data['email'])
        token = Token.objects.create(user=user)

        return Response(
            {
                'message': 'User created successfully',
                'token': token.key,
                'user': user_profile_serializer.data,
            }
        )
    
class UserProfileSignInView(APIView):
    serializer_class = serializers.UserProfileSerializer

    def post(self, request, format=None):
