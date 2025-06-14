from django.contrib import admin
from .models import Imovel, ImovelCliente

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'operacao', 'valor', 'status', 'corretor', 'data_cadastro')
    list_filter = ('tipo', 'operacao', 'status', 'corretor', 'data_cadastro')
    search_fields = ('titulo', 'endereco', 'descricao')
    ordering = ('-data_cadastro',)
    readonly_fields = ('data_cadastro', 'data_atualizacao')

@admin.register(ImovelCliente)
class ImovelClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'imovel', 'data_vinculo', 'tipo_imovel', 'operacao_imovel', 'valor_imovel')
    list_filter = ('data_vinculo', 'imovel__tipo', 'imovel__operacao')
    search_fields = ('cliente__first_name', 'cliente__last_name', 'cliente__email', 'imovel__titulo', 'imovel__endereco')
    ordering = ('-data_vinculo',)
    readonly_fields = ('data_vinculo',)

    def tipo_imovel(self, obj):
        return obj.imovel.get_tipo_display()
    tipo_imovel.short_description = 'Tipo do Imóvel'

    def operacao_imovel(self, obj):
        return obj.imovel.get_operacao_display()
    operacao_imovel.short_description = 'Operação'

    def valor_imovel(self, obj):
        return f'R$ {obj.imovel.valor}'
    valor_imovel.short_description = 'Valor'
