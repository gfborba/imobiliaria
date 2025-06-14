from django.db import models
from django.contrib.auth.models import User
from usuarios.models import CustomUser

# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=200)
    corretor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Imovel(models.Model):
    TIPO_CHOICES = [
        ('CASA', 'Casa'),
        ('APARTAMENTO', 'Apartamento'),
        ('COMERCIAL', 'Comercial'),
        ('TERRENO', 'Terreno'),
    ]
    
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('VENDIDO', 'Vendido'),
        ('ALUGADO', 'Alugado'),
    ]
    
    OPERACAO_CHOICES = [
        ('VENDA', 'Venda'),
        ('ALUGUEL', 'Aluguel'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    endereco = models.CharField(max_length=200)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    quartos = models.IntegerField()
    banheiros = models.IntegerField()
    vagas_garagem = models.IntegerField()
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIVEL')
    operacao = models.CharField(max_length=20, choices=OPERACAO_CHOICES)
    corretor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()} ({self.get_operacao_display()})"
