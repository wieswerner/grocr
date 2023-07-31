from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.boards),
    path('board/<str:id>', views.board),
    path('shopping-list/<str:card_ids>', views.shopping_list),
    path('shopping-list-ai/<str:card_ids>', views.shopping_list_ai),
    path('recipies/', views.recipies),
]
