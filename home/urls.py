from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(),name= "home"),
    # path("accounts/", include("django.contrib.auth.urls")),
]
