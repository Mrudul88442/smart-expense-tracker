from django.urls import path
from . import views

urlpatterns = [
    path('', views.todos_home, name='todos_home'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('add_todo/', views.add_todo, name='add_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
