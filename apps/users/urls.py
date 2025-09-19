from django.urls import path

from apps.core.views import about_view, welcome_view, declarants_view, DeclarantDetailUpdateView

# Оголошення простору імен
app_name = 'users'

urlpatterns = [
    # localhost:8000/users/
    # 'users:register'
    path('register/', welcome_view, name='register'),
]