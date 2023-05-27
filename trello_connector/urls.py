from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.boards),
    path('board/<str:id>', views.board),
    path('recipies/', views.recipies),
]
