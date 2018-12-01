from django.shortcuts import render,HttpResponse
from .serializers import UserSerializer,LoginSerializer,OrderSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from api.models import Order
from django.utils.timezone import localtime, now,timedelta
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'registration': reverse('user_registration', request=request, format=format),
        'login': reverse('login', request=request, format=format),
         # 'orders': reverse('orders', request=request, format=format),
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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def destroy(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        current_time=localtime(now())

        if current_time>order.created+timedelta(minutes=15):
            return Response({
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "code": "",
                "message": "You are not cancelled order right now.Already 15 minute gone",
                "error": {
                }
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        current_time = localtime(now())

        if current_time > order.created + timedelta(minutes=15):
            return Response({
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "code": "",
                "message": "You are not update order right now.Already 15 minute gone",
                "error": {
                }
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        return super().update(request, *args, **kwargs)


class OrderFilterListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset=queryset.filter(created__lte=end_date,created__gte=start_date)
        return queryset



