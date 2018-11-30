from django.urls import path,include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns=format_suffix_patterns([
    path('api-auth/', include('rest_framework.urls')),
    path('', views.api_root),
    path('registration/',views.UserRegistration.as_view(),name='user_registration'),
    path('login/', views.LoginView.as_view(), name='login'),



])