from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro-cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('dashboard/corretor/', views.dashboard_corretor, name='dashboard_corretor'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    
    #Gerenciamento de imóveis
    path('imoveis/cadastrar/', views.cadastrar_imovel, name='cadastrar_imovel'),
    path('imoveis/listar/', views.listar_imoveis, name='listar_imoveis'),
    path('interesses/', views.interesses, name='interesses'),
    
    #Gerenciamento de clientes
    path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    path('clientes/cadastrar/', views.cadastro_cliente, name='cadastro_cliente'),
    path('clientes/<int:cliente_id>/imoveis/', views.imoveis_cliente, name='imoveis_cliente'),
    path('clientes/<int:cliente_id>/atribuir-imovel/', views.atribuir_imovel, name='atribuir_imovel'),
    path('vinculos/<int:vinculo_id>/remover/', views.remover_vinculo, name='remover_vinculo'),
    path('imoveis/vinculados/', views.imoveis_vinculados, name='imoveis_vinculados'),
]