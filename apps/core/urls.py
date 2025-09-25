from django.urls import path

from apps.core.views import about_view, welcome_view, declarants_view, DeclarantDetailUpdateView, \
    declarants_search_view, declarations_analysis_view, add_declaration_view, add_declarant_view

urlpatterns = [
    path('',welcome_view, name='welcome'),
    path('about/',about_view, name='about'),
    path('declarants/',declarants_view, name='declarants'),
    path('declarants_search/',declarants_search_view, name='declarants_search'),
    path('declarations_analysis_page/',declarations_analysis_view, name='declarations_analysis_page'),
    path('declarants/<int:pk>/', DeclarantDetailUpdateView.as_view(), name='declarant_detail'),
    path("declarations/add/", add_declaration_view, name="add_declaration"),
    path("declarants/add/", add_declarant_view, name="add_declarant"),
    # path('declarant-form/', DeclarantDetailUpdateView.as_view(), name='declarant_form'),
]