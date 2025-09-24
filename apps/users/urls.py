from django.urls import path

import apps.users.views
#TODO IMPORT
from django.contrib.auth import views as auth_views

from apps.core.views import about_view
from apps.users import views

# Оголошення простору імен
# app_name = 'registration'

urlpatterns = [
    # localhost:8000/registration/
    # 'registration:register' #HTML...
    path('register/', apps.users.views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logged-out/', apps.users.views.logged_out_view, name='logged_out'),
    path('', apps.users.views.users_view, name='users'),
]