from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.api_boards),
    path('board/<str:id>', views.api_board),
    path('recipies/', views.recipies),
]