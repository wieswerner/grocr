from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.boards),
    path('board/<str:id>', views.board),
    path('shopping-list/<str:board_ids>', views.shopping_list),
    path('recipies/', views.recipies),
]
