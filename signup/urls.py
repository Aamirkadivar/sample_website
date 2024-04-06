from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('api/login/', views.UserLoginView.as_view(), name='api_login'),
    path('api/home/', views.HomeAPI.as_view(), name='api_home'),


]
urlpatterns += staticfiles_urlpatterns()
