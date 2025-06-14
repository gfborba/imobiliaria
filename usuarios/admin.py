from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'cpf', 'telefone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cpf', 'telefone')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Tipo de Usuário', {'fields': ('role',)}),
        ('Informações de Contato', {'fields': ('telefone', 'endereco')}),
        ('Informações do Cliente', {'fields': ('cpf',)}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name'),
        }),
        ('Tipo de Usuário', {
            'fields': ('role',),
        }),
        ('Informações de Contato', {
            'fields': ('telefone', 'endereco'),
        }),
        ('Informações do Cliente', {
            'fields': ('cpf',),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
