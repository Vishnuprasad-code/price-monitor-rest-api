from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from pm_api import models
from pm_api import serializers

from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

from django_celery_beat.models import PeriodicTask, IntervalSchedule


class HelloApiView(APIView):
    '''Test API view'''

    serializer_class = serializers.HelloSerializer
    def get(self, request, format=None):
        '''Returns a list of APIView features'''

        interval, _ = IntervalSchedule.objects.get_or_create(
            every=2,
            period=IntervalSchedule.SECONDS
        )
        
        PeriodicTask.objects.create(
            interval=interval,
            name='test_schedule*',
            task="pm_api.tasks.test_periodic_task",
        )

        return Response(
            {
                'message': 'Hello',
                # 'result': result
            }
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
    serializer_class = serializers.UserProfileModelSerializer

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
    serializer_class = serializers.UserProfileModelSerializer

    def post(self, request, format=None):
        user = get_object_or_404(get_user_model(), email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response(
                {
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        token, created = Token.objects.get_or_create(user=user)
        serializer = self.serializer_class(user)
        return Response(
            {
                'message': 'User signed in successfully',
                'token': token.key,
                'user': serializer.data
            }
        )


class WishlistView(APIView):
    product_serializer_class = serializers.ProductModelSerializer
    wishlist_serializer_class = serializers.WishlistModelSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    def post(self, request, format=None):
        user = get_user_model().objects.get(email=request.user.email)
        product, created = models.Product.objects.get_or_create(
            url=request.data['url'],
            name=request.data['name'],
        )
        
        models.Wishlist.objects.create(
            user=user,
            product=product
        )

        return Response(
            {
                'message': 'Product added to wishlist successfully',
            }
        )
    
    def get(self, request, format=None):
        user = get_user_model().objects.get(email=request.user.email)
        wishlist = user.user_wishlist_items.all()
        wishlist_serializer = self.wishlist_serializer_class(wishlist, many=True)
        return Response(
            {
                'message': 'Wishlisted products',
                'data': wishlist_serializer.data,
            }
        )


class ProductHistoryView(APIView):
    input_serializer_class = serializers.ProductHistorySerializer
    product_history_serializer_class = serializers.ProductHistoryModelSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    def post(self, request, format=None):
        input_serializer = self.input_serializer_class(data=request.data)
        if not input_serializer.is_valid():
            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        product_url = input_serializer.validated_data.get('url')
        product = models.Product.objects.get(url=product_url)
        product_history = product.product_price_histories.all()
        product_history_serializer = self.product_history_serializer_class(product_history, many=True)
        return Response(
            {
                'message': 'Product History',
                'data': product_history_serializer.data,
            }
        )
