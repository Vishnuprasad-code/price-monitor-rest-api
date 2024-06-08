from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from pm_api import serializers


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
