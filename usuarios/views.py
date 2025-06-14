from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser

def is_corretor(user):
    return user.is_corretor()

def is_cliente(user):
    return user.is_cliente()

def cadastro(request):
    if request.method == "GET":
        return render(request, 'pages/cadastro.html')
    else:
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        role = request.POST.get('role', 'CLIENTE')  # Default to CLIENTE if not specified

        if CustomUser.objects.filter(username=username).exists():
            contexto = {'useralredyexist': 'Usuário já existe'}
            return render(request, 'pages/cadastro.html', contexto)
        
        user = CustomUser.objects.create_user(
            username=username, 
            first_name=firstname, 
            last_name=lastname, 
            email=email, 
            password=senha,
            role=role
        )
        user.save()

        print('Cadastro realizado')
        return render(request, 'pages/login.html')

def login(request):
    if request.method == "GET":
        return render(request, 'pages/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        verificar_usuario = authenticate(username=username, password=senha)

        if verificar_usuario is not None:
            login_django(request, verificar_usuario)
            return redirect('index')
        else:
            contexto = {'error': 'Usuário ou senha incorretos'}
            return render(request, 'pages/login.html', contexto)

@login_required
def sair(request):
    logout(request)
    return render(request, 'pages/login.html')

@login_required
@user_passes_test(is_corretor)
def dashboard_corretor(request):
    # View for corretores to manage imoveis
    return render(request, 'pages/dashboard_corretor.html')

@login_required
@user_passes_test(is_cliente)
def dashboard_cliente(request):
    # View for clientes to view imoveis
    return render(request, 'pages/dashboard_cliente.html')