from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.expenses, name='expenses'),
    path('add-expense/',views.add_expense, name='add_expense'),
   path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),
]
