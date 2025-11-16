from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('chart-data/', views.chart_data, name='chart_data'),
]