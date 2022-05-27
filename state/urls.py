from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.ControlPage.as_view(), name="Control"),
    path('user', views.UserPage.as_view(), name="User"),
    path('usertwo', views.UserTwoPage.as_view(), name="User"),
    path('accounts/login/', views.Login.as_view(), name="Login"),
    path('register', views.Register.as_view(), name="Register"),
]
