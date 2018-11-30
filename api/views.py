from django.shortcuts import render,HttpResponse
from .serializers import UserSerializer,LoginSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status




# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'registration': reverse('user_registration', request=request, format=format),
        'login': reverse('login', request=request, format=format)
    })


class UserRegistration(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
#
#
class LoginView(APIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly)
    serializer_class = LoginSerializer

    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(email=email,password=password)
        if user:
            return Response({"token":user.auth_token.key})
        else:
            return Response({'error':'Wrong Credintial'},status=status.HTTP_400_BAD_REQUEST)