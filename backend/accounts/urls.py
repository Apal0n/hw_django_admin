from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view()),
    path('token/', obtain_auth_token),
    path('auth/', include('rest_framework.urls')),
]
