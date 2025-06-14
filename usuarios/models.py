from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        CORRETOR = 'CORRETOR', _('Corretor')
        CLIENTE = 'CLIENTE', _('Cliente')
    
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        verbose_name='Tipo de Usuário',
        help_text='Selecione se é Cliente ou Corretor'
    )
    
    def clean(self):
        super().clean()
        if self.role == self.Roles.CLIENTE:
            if not self.cpf:
                raise ValidationError({'cpf': 'CPF é obrigatório para clientes'})
            if not self.telefone:
                raise ValidationError({'telefone': 'Telefone é obrigatório para clientes'})
            if not self.endereco:
                raise ValidationError({'endereco': 'Endereço é obrigatório para clientes'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.role == self.Roles.CORRETOR:
            self.cpf = None
        super().save(*args, **kwargs)
    
    def is_corretor_user(self):
        return self.role == self.Roles.CORRETOR
    
    def is_cliente(self):
        return self.role == self.Roles.CLIENTE
