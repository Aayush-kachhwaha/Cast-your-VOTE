from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = "index page"),
    path('signup/', views.signup, name = "signup page"),
]
