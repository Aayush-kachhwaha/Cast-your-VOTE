from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = "index page"),
    path('signup/', views.signup, name = "signup page"),
    path('verify/', views.verify_code, name = "mobile verification"),
    path('landing/', views.landing, name = "initial landing page"),
    path('landing/home/', views.home, name = "home page"),
    path('landing/vote/<int:id>/', views.vote, name = "vote page"),
]
