from django.urls import path
from . import views

urlpatterns = [
    path('', views.target_dashboard, name='target_dashboard'),
    path('add/', views.add_target, name='add_target'),
    path('target/edit/<int:id>/', views.edit_target, name='edit_target'),
    path('target/delete/<int:id>/', views.delete_target, name='delete_target'),

]
