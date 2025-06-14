from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro-cliente/', views.cadastro_cliente, name='cadastro_cliente'),
]