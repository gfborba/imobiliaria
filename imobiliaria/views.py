from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from functools import wraps
from .models import Imovel, ImovelCliente, Interesse
from usuarios.models import CustomUser

#Página inicial
@login_required(login_url='/auth/login/')
def index(request):
    return render(request, 'pages/index.html')


#------------------LÓGICAS DE CLIENTE---------------------
def is_cliente(user):
    return user.is_cliente()

#Dashboard de clientes
@login_required
@user_passes_test(is_cliente, login_url=None)
def dashboard_cliente(request):
    return render(request, 'pages/cliente/dashboard_cliente.html')

#Interesses do cliente
@login_required
@user_passes_test(is_cliente, login_url=None)
def interesses(request):
    interesses = Interesse.objects.filter(cliente=request.user)
    return render(request, 'pages/cliente/interesses.html', {'interesses': interesses})

#Demonstrar interesse em um imóvel
@login_required
@user_passes_test(is_cliente, login_url=None)
def demonstrar_interesse(request, imovel_id):
    if request.method == "POST":
        imovel = get_object_or_404(Imovel, id=imovel_id)
        
        try:
            Interesse.objects.create(cliente=request.user, imovel=imovel)
            messages.success(request, f'Interesse registrado no imóvel "{imovel.titulo}"!')
        except Exception as e:
            messages.error(request, 'Você já demonstrou interesse neste imóvel.')
        
        return redirect('listar_imoveis')
    
    return redirect('listar_imoveis')

#Remover interesse em um imóvel
@login_required
@user_passes_test(is_cliente, login_url=None)
def remover_interesse(request, interesse_id):
    if request.method == "POST":
        interesse = get_object_or_404(Interesse, id=interesse_id, cliente=request.user)
        interesse.delete()
        messages.success(request, 'Interesse removido com sucesso!')
        return redirect('interesses')
    
    return redirect('interesses')

#Imóveis vinculados ao cliente
@login_required
@user_passes_test(is_cliente, login_url=None)
def imoveis_vinculados(request):
    imoveis = ImovelCliente.objects.filter(cliente=request.user)
    return render(request, 'pages/cliente/imoveis_vinculados.html', {'imoveis': imoveis})

#------------------FIM LÓGICAS DE CLIENTE---------------------

#------------------LÓGICAS DE CORRETOR---------------------
def is_corretor(user):
    return user.is_corretor_user()

#Verificar se o usuário é corretor e gerenciar seus acessos
def corretor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_corretor_user():
            return render(request, 'pages/erro_permissao.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


#Cadastro de clientes
@login_required(login_url='/auth/login/')
def cadastro_cliente(request):
    if not request.user.is_corretor_user():
        return render(request, 'pages/erro_permissao.html')
        
    if request.method == "POST":
        try:
            user = CustomUser.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('senha'),
                first_name=request.POST.get('firstname'),
                last_name=request.POST.get('lastname'),
                telefone=request.POST.get('telefone'),
                cpf=request.POST.get('cpf'),
                endereco=request.POST.get('endereco'),
                role='CLIENTE'
            )
            return redirect('index')
        except Exception as e:
            return render(request, 'pages/cadastro.html', {'error': 'Erro ao cadastrar cliente. Verifique se o email ou CPF já não estão cadastrados.'})
    
    return render(request, 'pages/cadastro.html')

#Dashboard do corretor
@corretor_required
def dashboard_corretor(request):
    return render(request, 'pages/corretor/dashboard_corretor.html')


#Cadastro de imóveis
@corretor_required
def cadastrar_imovel(request):
    if request.method == "POST":
        try:
            imovel = Imovel.objects.create(
                titulo=request.POST.get('titulo'),
                descricao=request.POST.get('descricao'),
                tipo=request.POST.get('tipo'),
                endereco=request.POST.get('endereco'),
                area=request.POST.get('area'),
                quartos=request.POST.get('quartos'),
                banheiros=request.POST.get('banheiros'),
                vagas_garagem=request.POST.get('vagas_garagem'),
                valor=request.POST.get('valor'),
                operacao=request.POST.get('operacao'),
                corretor=request.user
            )
            return redirect('listar_imoveis')
        except Exception as e:
            return render(request, 'pages/corretor/cadastrar_imovel.html', {'error': 'Erro ao cadastrar imóvel. Verifique se todos os campos foram preenchidos corretamente.'})
    
    return render(request, 'pages/corretor/cadastrar_imovel.html')

#Listagem de imóveis
@login_required
def listar_imoveis(request):
    imoveis = Imovel.objects.filter(status='DISPONIVEL')
    # Verificar quais imóveis o usuário já demonstrou interesse
    if request.user.is_cliente():
        interesses_usuario = Interesse.objects.filter(cliente=request.user)
        imoveis_com_interesse = [interesse.imovel.id for interesse in interesses_usuario]
    else:
        imoveis_com_interesse = []
    
    return render(request, 'pages/listar_imoveis.html', {
        'imoveis': imoveis,
        'imoveis_com_interesse': imoveis_com_interesse
    })


#Gerenciamento de clientes
@corretor_required
def listar_clientes(request):
    clientes = CustomUser.objects.filter(role='CLIENTE')
    imoveis_disponiveis = Imovel.objects.filter(status='DISPONIVEL')
    return render(request, 'pages/corretor/listar_clientes.html', {
        'clientes': clientes,
        'imoveis_disponiveis': imoveis_disponiveis
    })

#Imóveis atrelados ao cliente
@corretor_required
def imoveis_cliente(request, cliente_id):
    cliente = get_object_or_404(CustomUser, id=cliente_id, role='CLIENTE')
    imoveis = ImovelCliente.objects.filter(cliente=cliente)
    imoveis_vinculados = [vinculo.imovel.id for vinculo in imoveis]
    imoveis_disponiveis = Imovel.objects.filter(status='DISPONIVEL').exclude(id__in=imoveis_vinculados)
    return render(request, 'pages/corretor/imoveis_cliente.html', {
        'cliente': cliente,
        'imoveis': imoveis,
        'imoveis_disponiveis': imoveis_disponiveis
    })

#------RELAÇÃO DE IMÓVEIS E CLIENTES------
#Atribui um imovel ao cliente
@corretor_required
def atribuir_imovel(request, cliente_id):
    if request.method == "POST":
        cliente = get_object_or_404(CustomUser, id=cliente_id, role='CLIENTE')
        imovel_id = request.POST.get('imovel_id')
        imovel = get_object_or_404(Imovel, id=imovel_id)
        
        try:
            ImovelCliente.objects.create(cliente=cliente, imovel=imovel)
            messages.success(request, 'Imóvel atribuído com sucesso!')
        except Exception as e:
            messages.error(request, 'Este imóvel já está atribuído a este cliente.')
        
        return redirect('listar_clientes')
    
    return redirect('listar_clientes')

#Remove um imovel do cliente
@corretor_required
def remover_vinculo(request, vinculo_id):
    if request.method == "POST":
        vinculo = get_object_or_404(ImovelCliente, id=vinculo_id)
        cliente_id = vinculo.cliente.id
        vinculo.delete()
        messages.success(request, 'Vínculo removido com sucesso!')
        return redirect('imoveis_cliente', cliente_id=cliente_id)
    
    return redirect('listar_clientes')

#------------------FIM LÓGICAS DE CORRETOR---------------------