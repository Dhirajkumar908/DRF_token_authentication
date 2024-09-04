from django.urls import path
from account import views


urlpatterns=[
    path('login/', views.UserloginAPIview.as_view(), name='login'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout')
]

