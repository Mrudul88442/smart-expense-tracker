from django.urls import path
from . import views

urlpatterns = [
    path('', views.savings, name='savings'),
    path('add/', views.add_saving, name='add_saving'),
    path('edit/<int:id>/', views.edit_saving, name='edit_saving'),
    path('delete/<int:id>/', views.delete_saving, name='delete_saving'),
]
