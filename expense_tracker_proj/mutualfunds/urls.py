from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_funds, name='search_funds'),
    path('fund/<str:scheme_code>/', views.fund_detail, name='fund_detail'),
    path('', views.mutualfunds_dashboard, name='mutualfunds_dashboard'),
    path('add/<str:scheme_code>/', views.add_to_portfolio, name='add_to_portfolio'),
    path("portfolio/", views.my_portfolio, name="my_portfolio"),
    path('delete/<int:investment_id>/', views.delete_investment, name='delete_investment'),
    
]
