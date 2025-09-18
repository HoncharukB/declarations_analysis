from django.urls import path

from apps.core.views import about_view, welcome_view, declarants_view, DeclarantDetailUpdateView

urlpatterns = [
    path('',welcome_view, name='welcome'),
    path('about/',about_view, name='about'),
    path('declarants/',declarants_view, name='declarants'),
    path('declarants/<int:pk>/', DeclarantDetailUpdateView.as_view(), name='declarant_detail'),
    # path('declarant-form/', DeclarantDetailUpdateView.as_view(), name='declarant_form'),
]
