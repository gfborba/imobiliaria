from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('sair/', views.sair, name='sair'),
    path('dashboard/corretor/', views.dashboard_corretor, name='dashboard_corretor'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
]