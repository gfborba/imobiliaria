from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        CORRETOR = 'CORRETOR', _('Corretor')
        CLIENTE = 'CLIENTE', _('Cliente')
    
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.CLIENTE,
    )
    
    def is_corretor(self):
        return self.role == self.Roles.CORRETOR
    
    def is_cliente(self):
        return self.role == self.Roles.CLIENTE
