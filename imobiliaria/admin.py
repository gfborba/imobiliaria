from django.contrib import admin
from .models import Cliente, Imovel

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cpf', 'corretor', 'data_cadastro')
    list_filter = ('corretor', 'data_cadastro')
    search_fields = ('nome', 'email', 'cpf')
    ordering = ('-data_cadastro',)

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'operacao', 'valor', 'status', 'corretor', 'data_cadastro')
    list_filter = ('tipo', 'operacao', 'status', 'corretor', 'data_cadastro')
    search_fields = ('titulo', 'endereco', 'descricao')
    ordering = ('-data_cadastro',)
    readonly_fields = ('data_cadastro', 'data_atualizacao')
